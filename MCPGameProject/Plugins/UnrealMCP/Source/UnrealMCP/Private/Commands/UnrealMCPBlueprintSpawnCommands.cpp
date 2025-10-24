#include "Commands/UnrealMCPBlueprintSpawnCommands.h"
#include "Commands/UnrealMCPCommonUtils.h"
#include "Engine/Blueprint.h"
#include "Engine/BlueprintGeneratedClass.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "Editor.h"
#include "Kismet2/KismetEditorUtilities.h"
#include "Components/ActorComponent.h"
#include "SimpleConstructionScript.h"
#include "Kismet/GameplayStatics.h"

/**
 * Default constructor for the FUnrealMCPBlueprintSpawnCommands class.
 * Initializes the object and prepares it for use.
 *
 * @return An instance of FUnrealMCPBlueprintSpawnCommands.
 */
FUnrealMCPBlueprintSpawnCommands::FUnrealMCPBlueprintSpawnCommands() {
}

/**
 * 
 * @param Params 
 * @return 
 */
auto FUnrealMCPBlueprintSpawnCommands::HandleSpawnBlueprintActor(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Get required parameters
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName)) {
		return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	FString ActorName;
	if (!Params->TryGetStringField(TEXT("actor_name"), ActorName)) {
		return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Missing 'actor_name' parameter"));
	}

	// Find the blueprint
	UBlueprint* Blueprint = FUnrealMCPCommonUtils::FindBlueprint(BlueprintName);
	if (!Blueprint) {
		return FUnrealMCPCommonUtils::CreateErrorResponse(
			FString::Printf(TEXT("Blueprint not found: %s"), *BlueprintName));
	}

	// VALIDATION: Check if blueprint is properly compiled and has valid GeneratedClass
	if (!Blueprint->GeneratedClass) {
		UE_LOG(LogTemp, Error, TEXT("Blueprint '%s' has no GeneratedClass - attempting to compile"), *BlueprintName);

		// Try to compile the blueprint first
		FKismetEditorUtilities::CompileBlueprint(Blueprint);

		// Check again after compilation
		if (!Blueprint->GeneratedClass) {
			return FUnrealMCPCommonUtils::CreateErrorResponse(
				FString::Printf(TEXT("Blueprint '%s' failed to generate a valid class"), *BlueprintName));
		}
	}

	// VALIDATION: Check if the GeneratedClass is a valid Actor subclass
	if (!Blueprint->GeneratedClass->IsChildOf(AActor::StaticClass())) {
		return FUnrealMCPCommonUtils::CreateErrorResponse(
			FString::Printf(TEXT("Blueprint '%s' is not an Actor-based blueprint"), *BlueprintName));
	}

	// Get transform parameters
	FVector Location(0.0f, 0.0f, 0.0f);
	FRotator Rotation(0.0f, 0.0f, 0.0f);

	if (Params->HasField(TEXT("location"))) {
		Location = FUnrealMCPCommonUtils::GetVectorFromJson(Params, TEXT("location"));
	}
	if (Params->HasField(TEXT("rotation"))) {
		Rotation = FUnrealMCPCommonUtils::GetRotatorFromJson(Params, TEXT("rotation"));
	}

	// Get the world context
	UWorld* World = GEditor->GetEditorWorldContext().World();
	if (!World) {
		return FUnrealMCPCommonUtils::CreateErrorResponse(TEXT("Failed to get editor world"));
	}

	FTransform SpawnTransform;
	SpawnTransform.SetLocation(Location);
	SpawnTransform.SetRotation(FQuat(Rotation));

	UE_LOG(
		LogTemp,
		Log,
		TEXT("Spawning blueprint actor '%s' from blueprint '%s' at location (%s)"),
		*ActorName,
		*BlueprintName,
		*Location.ToString());

	if (AActor* NewActor = SpawnBlueprintActorSafely(Blueprint, ActorName, SpawnTransform, World)) {
		// Set the actor label explicitly (in addition to spawn name)
		NewActor->SetActorLabel(*ActorName);

		// The actor should be properly initialized after spawning
		// No additional initialization needed for blueprint actors

		UE_LOG(
			LogTemp,
			Log,
			TEXT("Blueprint actor '%s' spawned successfully at location (%s)"),
			*ActorName,
			*NewActor->GetActorLocation().ToString());

		return FUnrealMCPCommonUtils::ActorToJsonObject(NewActor, true);
	}

	FString ErrorMessage = FString::Printf(
		TEXT(
			"Failed to spawn blueprint actor '%s' - blueprint may have compilation errors or missing dependencies"),
		*BlueprintName);
	UE_LOG(LogTemp, Error, TEXT("%s"), *ErrorMessage);

	// Provide additional diagnostic information
	if (Blueprint->Status != BS_UpToDate) {
		ErrorMessage += TEXT(" (Blueprint compilation status: ");
		switch (Blueprint->Status) {
			case BS_Error:
				ErrorMessage += TEXT("Error)");
				break;
			case BS_Dirty:
				ErrorMessage += TEXT("Dirty/Needs Compile)");
				break;
			case BS_Unknown:
				ErrorMessage += TEXT("Unknown)");
				break;
			default:
				ErrorMessage += TEXT("Other)");
				break;
		}
	}

	return FUnrealMCPCommonUtils::CreateErrorResponse(ErrorMessage);
}

auto FUnrealMCPBlueprintSpawnCommands::SpawnBlueprintActorSafely(
	const UBlueprint* Blueprint,
	const FString& ActorName,
	const FTransform& SpawnTransform,
	UWorld* World
) -> AActor* {
	if (!Blueprint) {
		UE_LOG(LogTemp, Error, TEXT("SpawnBlueprintActorSafely: Invalid blueprint - null pointer"));
		return nullptr;
	}

	if (!World) {
		UE_LOG(LogTemp, Error, TEXT("SpawnBlueprintActorSafely: Invalid world context - null pointer"));
		return nullptr;
	}

	// Check blueprint compilation status first
	if (Blueprint->Status != BS_UpToDate) {
		UE_LOG(
			LogTemp,
			Error,
			TEXT("SpawnBlueprintActorSafely: Blueprint '%s' is not up to date (Status: %d)"),
			*Blueprint->GetName(),
			(int32)Blueprint->Status
		);

		// Provide detailed status information
		switch (Blueprint->Status) {
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

	if (!Blueprint->GeneratedClass) {
		UE_LOG(
			LogTemp,
			Error,
			TEXT(
				"SpawnBlueprintActorSafely: Blueprint '%s' has no generated class - blueprint may not be compiled properly"
			),
			*Blueprint->GetName()
		);
		return nullptr;
	}

	// Validate the generated class
	if (!Blueprint->GeneratedClass->IsChildOf<AActor>()) {
		UE_LOG(
			LogTemp,
			Error,
			TEXT("SpawnBlueprintActorSafely: Blueprint '%s' generated class is not a child of AActor"),
			*Blueprint->GetName()
		);
		return nullptr;
	}

	// Check for complex blueprint components that might cause timeouts
	bool bIsComplexBlueprint = false;
	FString ComplexityInfo;

	if (Blueprint->SimpleConstructionScript) {
		int32 ComponentCount = Blueprint->SimpleConstructionScript->GetAllNodes().Num();
		if (ComponentCount > 10) {
			bIsComplexBlueprint = true;
			ComplexityInfo = FString::Printf(TEXT("High component count: %d"), ComponentCount);
		}
	}

	// Check for timeline components (can cause spawning issues)
	if (Blueprint->Timelines.Num() > 0) {
		bIsComplexBlueprint = true;
		ComplexityInfo += FString::Printf(TEXT(" Timelines: %d"), Blueprint->Timelines.Num());
	}

	if (bIsComplexBlueprint) {
		UE_LOG(
			LogTemp,
			Warning,
			TEXT("SpawnBlueprintActorSafely: Blueprint '%s' appears complex (%s) - spawn may take longer"),
			*Blueprint->GetName(),
			*ComplexityInfo
		);
	}

	// Set up spawn parameters
	FActorSpawnParameters SpawnParams;
	SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;

	// Check if name is already in use and modify if necessary
	FString FinalActorName = ActorName;

	// Get all actors to check if name is already in use
	TArray<AActor*> AllActors;
	UGameplayStatics::GetAllActorsOfClass(World, AActor::StaticClass(), AllActors);

	for (const AActor* ExistingActor : AllActors) {
		if (ExistingActor && ExistingActor->GetActorLabel().Equals(FinalActorName)) {
			UE_LOG(
				LogTemp,
				Warning,
				TEXT("SpawnBlueprintActorSafely: Actor name '%s' already exists, appending timestamp"),
				*FinalActorName
			);
			const FDateTime Now = FDateTime::Now();
			FinalActorName = FString::Printf(TEXT("%s_%d"), *FinalActorName, Now.GetTicks());
			break;
		}
	}
	SpawnParams.Name = FName(*FinalActorName);

	UE_LOG(
		LogTemp,
		Log,
		TEXT("SpawnBlueprintActorSafely: Attempting to spawn '%s' from blueprint '%s'"),
		*FinalActorName,
		*Blueprint->GetName());

	AActor* NewActor = World->SpawnActor<AActor>(Blueprint->GeneratedClass, SpawnTransform, SpawnParams);

	if (NewActor) {
		// Set the actor label explicitly
		NewActor->SetActorLabel(FinalActorName);

		UE_LOG(
			LogTemp,
			Log,
			TEXT("SpawnBlueprintActorSafely: Successfully spawned blueprint actor '%s' (Class: %s)"),
			*FinalActorName,
			*NewActor->GetClass()->GetName()
		);
	}
	else {
		UE_LOG(
			LogTemp,
			Error,
			TEXT("SpawnBlueprintActorSafely: Failed to spawn blueprint actor '%s'"),
			*FinalActorName);
		UE_LOG(LogTemp, Error, TEXT("  Blueprint: %s"), *Blueprint->GetName());
		UE_LOG(LogTemp, Error, TEXT("  Spawn Location: %s"), *SpawnTransform.GetLocation().ToString());
		UE_LOG(LogTemp, Error, TEXT("  Generated Class: %s"), *Blueprint->GeneratedClass->GetName());
		UE_LOG(LogTemp, Error, TEXT("  World Context: %s"), World ? *World->GetName() : TEXT("None"));

		// Additional diagnostic information
		if (Blueprint->SimpleConstructionScript) {
			UE_LOG(
				LogTemp,
				Error,
				TEXT("  SCS Components: %d"),
				Blueprint->SimpleConstructionScript->GetAllNodes().Num());
		}
		UE_LOG(
			LogTemp,
			Error,
			TEXT("  Parent Class: %s"),
			Blueprint->ParentClass ? *Blueprint->ParentClass->GetName() : TEXT("None"));
	}

	return NewActor;
}
