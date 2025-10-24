#include "Services/BlueprintCreationService.h"
#include "Commands/UnrealMCPCommonUtils.h"
#include "Engine/Blueprint.h"
#include "Engine/BlueprintGeneratedClass.h"
#include "Factories/BlueprintFactory.h"
#include "Kismet2/KismetEditorUtilities.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Pawn.h"
#include "EditorAssetLibrary.h"

namespace UnrealMCP
{
	TResult<UBlueprint*> FBlueprintCreationService::CreateBlueprint(const FBlueprintCreationParams& Params)
	{
		if (Params.Name.IsEmpty())
		{
			return TResult<UBlueprint*>::Failure(TEXT("Blueprint name cannot be empty"));
		}

		const FString FullAssetPath = Params.PackagePath + Params.Name;

		// Check if asset already exists
		if (UEditorAssetLibrary::DoesAssetExist(FullAssetPath))
		{
			return TResult<UBlueprint*>::Failure(
				FString::Printf(TEXT("Blueprint already exists: %s"), *Params.Name)
			);
		}

		// Resolve parent class
		UClass* ParentClass = ResolveParentClass(Params.ParentClass);
		if (!ParentClass)
		{
			return TResult<UBlueprint*>::Failure(
				FString::Printf(TEXT("Failed to resolve parent class: %s"), *Params.ParentClass)
			);
		}

		// Create blueprint factory
		UBlueprintFactory* Factory = NewObject<UBlueprintFactory>();
		if (!Factory)
		{
			return TResult<UBlueprint*>::Failure(TEXT("Failed to create blueprint factory"));
		}

		Factory->ParentClass = ParentClass;

		// Create package
		UPackage* Package = CreatePackage(*FullAssetPath);
		if (!Package)
		{
			return TResult<UBlueprint*>::Failure(
				FString::Printf(TEXT("Failed to create package: %s"), *FullAssetPath)
			);
		}

		// Create blueprint using factory
		UBlueprint* NewBlueprint = Cast<UBlueprint>(
			Factory->FactoryCreateNew(
				UBlueprint::StaticClass(),
				Package,
				*Params.Name,
				RF_Standalone | RF_Public,
				nullptr,
				GWarn
			)
		);

		if (!NewBlueprint)
		{
			return TResult<UBlueprint*>::Failure(TEXT("Failed to create blueprint asset"));
		}

		// Register with asset registry and mark as dirty
		FAssetRegistryModule::AssetCreated(NewBlueprint);
		Package->MarkPackageDirty();

		return TResult<UBlueprint*>::Success(NewBlueprint);
	}

	TSharedPtr<FJsonObject> FBlueprintCreationService::CreateBlueprintAsJson(const FBlueprintCreationParams& Params)
	{
		TResult<UBlueprint*> Result = CreateBlueprint(Params);

		if (Result.IsSuccess())
		{
			UBlueprint* Blueprint = Result.GetValue();
			TSharedPtr<FJsonObject> ResponseObj = MakeShared<FJsonObject>();
			ResponseObj->SetStringField(TEXT("name"), Params.Name);
			ResponseObj->SetStringField(TEXT("path"), Params.PackagePath + Params.Name);
			ResponseObj->SetStringField(TEXT("parent_class"), Blueprint->ParentClass ? *Blueprint->ParentClass->GetName() : TEXT("AActor"));
			ResponseObj->SetBoolField(TEXT("success"), true);
			return ResponseObj;
		}

		return CreateErrorResponse(Result.GetError());
	}

	FVoidResult FBlueprintCreationService::CompileBlueprint(const FString& BlueprintName)
	{
		if (BlueprintName.IsEmpty())
		{
			return FVoidResult::Failure(TEXT("Blueprint name cannot be empty"));
		}

		UBlueprint* Blueprint = FUnrealMCPCommonUtils::FindBlueprint(BlueprintName);
		if (!Blueprint)
		{
			return FVoidResult::Failure(
				FString::Printf(TEXT("Blueprint not found: %s"), *BlueprintName)
			);
		}

		// Attempt compilation
		FKismetEditorUtilities::CompileBlueprint(Blueprint);

		// Check compilation result
		if (Blueprint->Status == BS_Error)
		{
			return FVoidResult::Failure(
				FString::Printf(TEXT("Blueprint compilation failed for: %s"), *BlueprintName)
			);
		}

		return FVoidResult::Success();
	}

	TSharedPtr<FJsonObject> FBlueprintCreationService::CompileBlueprintAsJson(const FString& BlueprintName)
	{
		FVoidResult Result = CompileBlueprint(BlueprintName);

		if (Result.IsSuccess())
		{
			TSharedPtr<FJsonObject> ResponseObj = MakeShared<FJsonObject>();
			ResponseObj->SetStringField(TEXT("name"), BlueprintName);
			ResponseObj->SetBoolField(TEXT("compiled"), true);
			ResponseObj->SetBoolField(TEXT("success"), true);
			return ResponseObj;
		}

		return CreateErrorResponse(Result.GetError());
	}

	UClass* FBlueprintCreationService::ResolveParentClass(const FString& ParentClassName)
	{
		if (ParentClassName.IsEmpty())
		{
			return AActor::StaticClass();
		}

		FString ClassName = ParentClassName;

		// Attempt direct class resolution for common cases
		if (ClassName == TEXT("Pawn"))
		{
			return APawn::StaticClass();
		}

		if (ClassName == TEXT("Actor") || ClassName.IsEmpty())
		{
			return AActor::StaticClass();
		}

		// Add 'A' prefix if not present
		if (!ClassName.StartsWith(TEXT("A")))
		{
			ClassName = TEXT("A") + ClassName;
		}

		// Attempt to load from Engine module
		if (ClassName == TEXT("APawn"))
		{
			return APawn::StaticClass();
		}

		if (ClassName == TEXT("AActor"))
		{
			return AActor::StaticClass();
		}

		const FString EngineClassPath = FString::Printf(TEXT("/Script/Engine.%s"), *ClassName);
		UClass* FoundClass = LoadClass<AActor>(nullptr, *EngineClassPath);

		if (FoundClass)
		{
			UE_LOG(LogTemp, Log, TEXT("Resolved parent class to '%s' from Engine module"), *ClassName);
			return FoundClass;
		}

		// Attempt to load from Game module
		const FString GameClassPath = FString::Printf(TEXT("/Script/Game.%s"), *ClassName);
		FoundClass = LoadClass<AActor>(nullptr, *GameClassPath);

		if (FoundClass)
		{
			UE_LOG(LogTemp, Log, TEXT("Resolved parent class to '%s' from Game module"), *ClassName);
			return FoundClass;
		}

		// Log warning and fallback to AActor
		UE_LOG(
			LogTemp,
			Warning,
			TEXT("Could not find parent class '%s' (tried: %s and %s) - defaulting to AActor"),
			*ParentClassName,
			*EngineClassPath,
			*GameClassPath
		);

		return AActor::StaticClass();
	}

	TSharedPtr<FJsonObject> FBlueprintCreationService::CreateErrorResponse(const FString& Error)
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(Error);
	}

	TSharedPtr<FJsonObject> FBlueprintCreationService::CreateSuccessResponse(const TSharedPtr<FJsonObject>& Data)
	{
		if (Data)
		{
			return Data;
		}

		TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
		Response->SetBoolField(TEXT("success"), true);
		return Response;
	}
}
