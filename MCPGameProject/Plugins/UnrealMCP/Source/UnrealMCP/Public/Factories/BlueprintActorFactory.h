#pragma once

#include "CoreMinimal.h"
#include "Core/Result.h"

class UBlueprint;
class UWorld;
class AActor;

namespace UnrealMCP
{
	/**
	 * Factory for spawning actors from blueprints
	 * Handles validation, safety checks, and proper actor initialization
	 */
	class UNREALMCP_API FBlueprintActorFactory
	{
	public:
		/**
		 * Spawn an actor from a blueprint with comprehensive validation
		 * @param Blueprint The blueprint to spawn from (must be valid and compiled)
		 * @param ActorName The name to give the spawned actor
		 * @param Transform The transform to spawn at
		 * @param World The world to spawn in (must be valid)
		 * @return Result containing the spawned actor or an error message
		 */
		static TResult<AActor*> SpawnFromBlueprint(
			const UBlueprint* Blueprint,
			const FString& ActorName,
			const FTransform& Transform,
			UWorld* World
		);

	private:
		/** Validate blueprint is ready for spawning */
		static FVoidResult ValidateBlueprint(const UBlueprint* Blueprint);

		/** Check for potential complexity issues */
		static void LogComplexityWarnings(const UBlueprint* Blueprint);

		/** Generate a unique actor name if the requested one is taken */
		static FString EnsureUniqueActorName(const FString& DesiredName, UWorld* World);
	};
}
