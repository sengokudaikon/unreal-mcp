#include "Commands/UnrealMCPBlueprintCreationCommands.h"
#include "Commands/UnrealMCPCommonUtils.h"
#include "Engine/Blueprint.h"
#include "Engine/BlueprintGeneratedClass.h"
#include "Factories/BlueprintFactory.h"
#include "Kismet2/KismetEditorUtilities.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Pawn.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "Editor.h"

auto FUnrealMCPBlueprintCreationCommands::HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>
{
	if (CommandType == TEXT("create_blueprint"))
	{
		return HandleCreateBlueprint(Params);
	}
	if (CommandType == TEXT("compile_blueprint"))
	{
		return HandleCompileBlueprint(Params);
	}
	if (CommandType == TEXT("spawn_blueprint_actor"))
	{
		return HandleSpawnBlueprintActor(Params);
	}

	return FUnrealMCPCommonUtils::CreateErrorResponse(
		FString::Printf(TEXT("Unknown blueprint creation command: %s"), *CommandType));
}

auto FUnrealMCPBlueprintCreationCommands::HandleCreateBlueprint(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>
{
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("name"), BlueprintName))
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'name' parameter"));
	}

	FString PackagePath = TEXT("/Game/Blueprints/");
	FString AssetName = BlueprintName;
	if (UEditorAssetLibrary::DoesAssetExist(PackagePath + AssetName))
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Blueprint already exists: %s"), *BlueprintName));
	}

	UBlueprintFactory* Factory = NewObject<UBlueprintFactory>();

	FString ParentClass;
	Params->TryGetStringField(TEXT("parent_class"), ParentClass);

	UClass* SelectedParentClass = FindParentClass(ParentClass);
	Factory->ParentClass = SelectedParentClass;

	UPackage* Package = CreatePackage(*(PackagePath + AssetName));
	UBlueprint* NewBlueprint = Cast<UBlueprint>(Factory->FactoryCreateNew(UBlueprint::StaticClass(), Package, *AssetName, RF_Standalone | RF_Public, nullptr, GWarn));

	if (NewBlueprint)
	{
		FAssetRegistryModule::AssetCreated(NewBlueprint);
		Package->MarkPackageDirty();

		TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
		ResultObj->SetStringField(TEXT("name"), AssetName);
		ResultObj->SetStringField(TEXT("path"), PackagePath + AssetName);
		return ResultObj;
	}

	return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to create blueprint"));
}

auto FUnrealMCPBlueprintCreationCommands::HandleCompileBlueprint(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>
{
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName))
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	UBlueprint* Blueprint = FUnrealMCPCommonUtils::FindBlueprint(BlueprintName);
	if (!Blueprint)
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Blueprint not found: %s"), *BlueprintName));
	}

	FKismetEditorUtilities::CompileBlueprint(Blueprint);

	TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
	ResultObj->SetStringField(TEXT("name"), BlueprintName);
	ResultObj->SetBoolField(TEXT("compiled"), true);
	return ResultObj;
}

auto FUnrealMCPBlueprintCreationCommands::HandleSpawnBlueprintActor(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>
{
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName))
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	FString ActorName;
	if (!Params->TryGetStringField(TEXT("actor_name"), ActorName))
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'actor_name' parameter"));
	}

	UBlueprint* Blueprint = FUnrealMCPCommonUtils::FindBlueprint(BlueprintName);
	if (!Blueprint)
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Blueprint not found: %s"), *BlueprintName));
	}

	if (!Blueprint->GeneratedClass)
	{
		UE_LOG(LogTemp, Error, TEXT("Blueprint '%s' has no GeneratedClass - attempting to compile"), *BlueprintName);
		FKismetEditorUtilities::CompileBlueprint(Blueprint);

		if (!Blueprint->GeneratedClass)
		{
			return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Blueprint '%s' failed to generate a valid class"), *BlueprintName));
		}
	}

	if (!Blueprint->GeneratedClass->IsChildOf(AActor::StaticClass()))
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Blueprint '%s' is not an Actor-based blueprint"), *BlueprintName));
	}

	FVector Location(0.0f, 0.0f, 0.0f);
	FRotator Rotation(0.0f, 0.0f, 0.0f);

	if (Params->HasField(TEXT("location")))
	{
		Location = FUnrealMCPCommonUtils::GetVectorFromJson(Params, TEXT("location"));
	}
	if (Params->HasField(TEXT("rotation")))
	{
		Rotation = FUnrealMCPCommonUtils::GetRotatorFromJson(Params, TEXT("rotation"));
	}

	UWorld* World = GEditor->GetEditorWorldContext().World();
	if (!World)
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get editor world"));
	}

	FTransform SpawnTransform;
	SpawnTransform.SetLocation(Location);
	SpawnTransform.SetRotation(FQuat(Rotation));

	AActor* NewActor = SpawnBlueprintActorSafely(Blueprint, ActorName, SpawnTransform, World);

	if (NewActor)
	{
		NewActor->SetActorLabel(*ActorName);

		if (!NewActor->IsActorInitialized())
		{
			NewActor->InitializeActor();
		}

		return FUnrealMCPCommonUtils::ActorToJsonObject(NewActor, true);
	}
	else
	{
		FString ErrorMessage = FString::Printf(TEXT("Failed to spawn blueprint actor '%s' - blueprint may have compilation errors or missing dependencies"), *BlueprintName);
		UE_LOG(LogTemp, Error, TEXT("%s"), *ErrorMessage);

		if (Blueprint->Status != BS_UpToDate)
		{
			ErrorMessage += TEXT(" (Blueprint compilation status: ");
			switch (Blueprint->Status)
			{
			case BS_Error: ErrorMessage += TEXT("Error)"); break;
			case BS_Dirty: ErrorMessage += TEXT("Dirty/Needs Compile)"); break;
			case BS_Unknown: ErrorMessage += TEXT("Unknown)"); break;
			default: ErrorMessage += TEXT("Other)"); break;
			}
		}

		return FUnrealMCPCommonUtils::CreateErrorResponse(ErrorMessage);
	}
}

AActor* FUnrealMCPBlueprintCreationCommands::SpawnBlueprintActorSafely(UBlueprint* Blueprint, const FString& ActorName, const FTransform& SpawnTransform, UWorld* World)
{
	if (!Blueprint)
	{
		UE_LOG(LogTemp, Error, TEXT("SpawnBlueprintActorSafely: Invalid blueprint - null pointer"));
		return nullptr;
	}

	if (!World)
	{
		UE_LOG(LogTemp, Error, TEXT("SpawnBlueprintActorSafely: Invalid world context - null pointer"));
		return nullptr;
	}

	if (Blueprint->Status != BS_UpToDate)
	{
		UE_LOG(LogTemp, Error, TEXT("SpawnBlueprintActorSafely: Blueprint '%s' is not up to date (Status: %d)"), *Blueprint->GetName(), (int32)Blueprint->Status);

		switch (Blueprint->Status)
		{
		case BS_Unknown:
			UE_LOG(LogTemp, Error, TEXT("  Status: Unknown - blueprint may be corrupted"));
			break;
		case BS_Dirty:
			UE_LOG(LogTemp, Error, TEXT("  Status: Dirty - blueprint has unsaved changes"));
			break;
		case BS_Error:
			UE_LOG(LogTemp, Error, TEXT("  Status: Error - blueprint has compilation errors"));
			break;
		case BS_BeingCreated:
			UE_LOG(LogTemp, Error, TEXT("  Status: Being Created - blueprint is still being created"));
			break;
		default:
			UE_LOG(LogTemp, Error, TEXT("  Status: Other (%d)"), (int32)Blueprint->Status);
			break;
		}
		return nullptr;
	}

	if (!Blueprint->GeneratedClass)
	{
		UE_LOG(LogTemp, Error, TEXT("SpawnBlueprintActorSafely: Blueprint '%s' has no generated class - blueprint may not be compiled properly"), *Blueprint->GetName());
		return nullptr;
	}

	if (!Blueprint->GeneratedClass->IsChildOf<AActor>())
	{
		UE_LOG(LogTemp, Error, TEXT("SpawnBlueprintActorSafely: Blueprint '%s' generated class is not a child of AActor"), *Blueprint->GetName());
		return nullptr;
	}

	bool bIsComplexBlueprint = false;
	FString ComplexityInfo;

	if (Blueprint->SimpleConstructionScript)
	{
		int32 ComponentCount = Blueprint->SimpleConstructionScript->GetAllNodes().Num();
		if (ComponentCount > 10)
		{
			bIsComplexBlueprint = true;
			ComplexityInfo = FString::Printf(TEXT("High component count: %d"), ComponentCount);
		}
	}

	if (Blueprint->Timelines.Num() > 0)
	{
		bIsComplexBlueprint = true;
		ComplexityInfo += FString::Printf(TEXT(" Timelines: %d"), Blueprint->Timelines.Num());
	}

	if (bIsComplexBlueprint)
	{
		UE_LOG(LogTemp, Warning, TEXT("SpawnBlueprintActorSafely: Blueprint '%s' appears complex (%s) - spawn may take longer"),
			*Blueprint->GetName(), *ComplexityInfo);
	}

	FActorSpawnParameters SpawnParams;
	SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

	FString FinalActorName = ActorName;
	if (!World->IsActorNameAvailable(FName(*FinalActorName)))
	{
		UE_LOG(LogTemp, Warning, TEXT("SpawnBlueprintActorSafely: Actor name '%s' already exists, appending timestamp"), *FinalActorName);
		const FDateTime Now = FDateTime::Now();
		FinalActorName = FString::Printf(TEXT("%s_%d"), *FinalActorName, Now.GetTicks());
	}
	SpawnParams.Name = FName(*FinalActorName);

	UE_LOG(LogTemp, Log, TEXT("SpawnBlueprintActorSafely: Attempting to spawn '%s' from blueprint '%s'"), *FinalActorName, *Blueprint->GetName());

	AActor* NewActor = World->SpawnActor<AActor>(Blueprint->GeneratedClass, SpawnTransform, SpawnParams);

	if (NewActor)
	{
		NewActor->SetActorLabel(FinalActorName);

		UE_LOG(LogTemp, Log, TEXT("SpawnBlueprintActorSafely: Successfully spawned blueprint actor '%s' (Class: %s)"),
			*FinalActorName, *NewActor->GetClass()->GetName());
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("SpawnBlueprintActorSafely: Failed to spawn blueprint actor '%s'"), *FinalActorName);
		UE_LOG(LogTemp, Error, TEXT("  Blueprint: %s"), *Blueprint->GetName());
		UE_LOG(LogTemp, Error, TEXT("  Spawn Location: %s"), *SpawnTransform.GetLocation().ToString());
		UE_LOG(LogTemp, Error, TEXT("  Generated Class: %s"), *Blueprint->GeneratedClass->GetName());
		UE_LOG(LogTemp, Error, TEXT("  World Context: %s"), World ? *World->GetName() : TEXT("None"));

		if (Blueprint->SimpleConstructionScript)
		{
			UE_LOG(LogTemp, Error, TEXT("  SCS Components: %d"), Blueprint->SimpleConstructionScript->GetAllNodes().Num());
		}
		UE_LOG(LogTemp, Error, TEXT("  Parent Class: %s"), Blueprint->ParentClass ? *Blueprint->ParentClass->GetName() : TEXT("None"));
	}

	return NewActor;
}

UClass* FUnrealMCPBlueprintCreationCommands::FindParentClass(const FString& ParentClassName)
{
	if (ParentClassName.IsEmpty())
	{
		return AActor::StaticClass();
	}

	FString ClassName = ParentClassName;
	if (!ClassName.StartsWith(TEXT("A")))
	{
		ClassName = TEXT("A") + ClassName;
	}

	UClass* FoundClass = nullptr;
	if (ClassName == TEXT("APawn"))
	{
		FoundClass = APawn::StaticClass();
	}
	else if (ClassName == TEXT("AActor"))
	{
		FoundClass = AActor::StaticClass();
	}
	else
	{
		const FString ClassPath = FString::Printf(TEXT("/Script/Engine.%s"), *ClassName);
		FoundClass = LoadClass<AActor>(nullptr, *ClassPath);

		if (!FoundClass)
		{
			const FString GameClassPath = FString::Printf(TEXT("/Script/Game.%s"), *ClassName);
			FoundClass = LoadClass<AActor>(nullptr, *GameClassPath);
		}
	}

	if (FoundClass)
	{
		UE_LOG(LogTemp, Log, TEXT("Successfully set parent class to '%s'"), *ClassName);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Could not find specified parent class '%s' at paths: /Script/Engine.%s or /Script/Game.%s, defaulting to AActor"),
			*ClassName, *ClassName, *ClassName);
		return AActor::StaticClass();
	}

	return FoundClass;
}