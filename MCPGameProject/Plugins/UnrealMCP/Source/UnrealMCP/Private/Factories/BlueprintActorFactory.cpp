#include "Factories/BlueprintActorFactory.h"
#include "Engine/Blueprint.h"
#include "Engine/BlueprintGeneratedClass.h"
#include "Engine/World.h"
#include "Engine/SimpleConstructionScript.h"
#include "GameFramework/Actor.h"
#include "Kismet/GameplayStatics.h"

namespace UnrealMCP
{
	TResult<AActor*> FBlueprintActorFactory::SpawnFromBlueprint(
		const UBlueprint* Blueprint,
		const FString& ActorName,
		const FTransform& Transform,
		UWorld* World)
	{
		// Validate inputs
		if (!Blueprint)
		{
			return TResult<AActor*>::Failure(TEXT("Invalid blueprint - null pointer"));
		}

		if (!World)
		{
			return TResult<AActor*>::Failure(TEXT("Invalid world context - null pointer"));
		}

		// Validate blueprint is ready for spawning
		FVoidResult ValidationResult = ValidateBlueprint(Blueprint);
		if (ValidationResult.IsFailure())
		{
			return TResult<AActor*>::Failure(ValidationResult.GetError());
		}

		// Log complexity warnings if needed
		LogComplexityWarnings(Blueprint);

		// Ensure unique actor name
		FString FinalActorName = EnsureUniqueActorName(ActorName, World);

		// Set up spawn parameters
		FActorSpawnParameters SpawnParams;
		SpawnParams.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
		SpawnParams.Name = FName(*FinalActorName);

		UE_LOG(LogTemp, Log, TEXT("FBlueprintActorFactory: Attempting to spawn '%s' from blueprint '%s'"),
			*FinalActorName, *Blueprint->GetName());

		// Spawn the actor
		AActor* NewActor = World->SpawnActor<AActor>(Blueprint->GeneratedClass, Transform, SpawnParams);

		if (!NewActor)
		{
			// Provide comprehensive error information
			FString ErrorMsg = FString::Printf(
				TEXT("Failed to spawn actor '%s' from blueprint '%s'. Spawn Location: %s, Generated Class: %s"),
				*FinalActorName,
				*Blueprint->GetName(),
				*Transform.GetLocation().ToString(),
				*Blueprint->GeneratedClass->GetName()
			);

			UE_LOG(LogTemp, Error, TEXT("FBlueprintActorFactory: %s"), *ErrorMsg);

			if (Blueprint->SimpleConstructionScript)
			{
				UE_LOG(LogTemp, Error, TEXT("  SCS Components: %d"),
					Blueprint->SimpleConstructionScript->GetAllNodes().Num());
			}

			return TResult<AActor*>::Failure(ErrorMsg);
		}

		// Set the actor label explicitly
		NewActor->SetActorLabel(FinalActorName);

		UE_LOG(LogTemp, Log, TEXT("FBlueprintActorFactory: Successfully spawned '%s' (Class: %s)"),
			*FinalActorName, *NewActor->GetClass()->GetName());

		return TResult<AActor*>::Success(NewActor);
	}

	FVoidResult FBlueprintActorFactory::ValidateBlueprint(const UBlueprint* Blueprint)
	{
		// Check compilation status
		if (Blueprint->Status != BS_UpToDate)
		{
			FString StatusMsg;
			switch (Blueprint->Status)
			{
			case BS_Unknown:
				StatusMsg = TEXT("Unknown - blueprint may be corrupted");
				break;
			case BS_Dirty:
				StatusMsg = TEXT("Dirty - blueprint has unsaved changes");
				break;
			case BS_Error:
				StatusMsg = TEXT("Error - blueprint has compilation errors");
				break;
			case BS_BeingCreated:
				StatusMsg = TEXT("Being Created - blueprint is still being created");
				break;
			default:
				StatusMsg = FString::Printf(TEXT("Other (%d)"), static_cast<int32>(Blueprint->Status));
				break;
			}

			return FVoidResult::Failure(
				FString::Printf(TEXT("Blueprint '%s' is not up to date. Status: %s"),
					*Blueprint->GetName(), *StatusMsg)
			);
		}

		// Check generated class
		if (!Blueprint->GeneratedClass)
		{
			return FVoidResult::Failure(
				FString::Printf(TEXT("Blueprint '%s' has no generated class - may not be compiled properly"),
					*Blueprint->GetName())
			);
		}

		// Validate it's an Actor blueprint
		if (!Blueprint->GeneratedClass->IsChildOf<AActor>())
		{
			return FVoidResult::Failure(
				FString::Printf(TEXT("Blueprint '%s' is not an Actor-based blueprint"),
					*Blueprint->GetName())
			);
		}

		return FVoidResult::Success();
	}

	void FBlueprintActorFactory::LogComplexityWarnings(const UBlueprint* Blueprint)
	{
		bool bIsComplex = false;
		FString ComplexityInfo;

		// Check component count
		if (Blueprint->SimpleConstructionScript)
		{
			int32 ComponentCount = Blueprint->SimpleConstructionScript->GetAllNodes().Num();
			if (ComponentCount > 10)
			{
				bIsComplex = true;
				ComplexityInfo = FString::Printf(TEXT("High component count: %d"), ComponentCount);
			}
		}

		// Check timeline count
		if (Blueprint->Timelines.Num() > 0)
		{
			bIsComplex = true;
			if (!ComplexityInfo.IsEmpty())
			{
				ComplexityInfo += TEXT(", ");
			}
			ComplexityInfo += FString::Printf(TEXT("Timelines: %d"), Blueprint->Timelines.Num());
		}

		if (bIsComplex)
		{
			UE_LOG(LogTemp, Warning,
				TEXT("FBlueprintActorFactory: Blueprint '%s' appears complex (%s) - spawn may take longer"),
				*Blueprint->GetName(), *ComplexityInfo);
		}
	}

	FString FBlueprintActorFactory::EnsureUniqueActorName(const FString& DesiredName, UWorld* World)
	{
		// Get all actors to check if name is already in use
		TArray<AActor*> AllActors;
		UGameplayStatics::GetAllActorsOfClass(World, AActor::StaticClass(), AllActors);

		for (const AActor* ExistingActor : AllActors)
		{
			if (ExistingActor && ExistingActor->GetActorLabel().Equals(DesiredName))
			{
				// Name collision - append timestamp
				FString UniqueName = FString::Printf(TEXT("%s_%lld"),
					*DesiredName,
					FDateTime::Now().GetTicks());

				UE_LOG(LogTemp, Warning,
					TEXT("FBlueprintActorFactory: Actor name '%s' already exists, using '%s'"),
					*DesiredName, *UniqueName);

				return UniqueName;
			}
		}

		return DesiredName;
	}
}
