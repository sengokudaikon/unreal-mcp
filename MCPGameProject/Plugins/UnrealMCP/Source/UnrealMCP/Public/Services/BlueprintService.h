#pragma once

#include "CoreMinimal.h"
#include "Core/Result.h"
#include "Core/MCPTypes.h"
#include "Json.h"

class UBlueprint;
class AActor;

namespace UnrealMCP {
	/**
	 * High-level service for blueprint operations
	 * Coordinates between factories, utilities, and the Unreal Editor APIs
	 */
	class UNREALMCP_API FBlueprintService {
	public:
		// Spawning operations
		static auto SpawnActor(const FBlueprintSpawnParams& Params) -> TResult<AActor*>;

		auto SpawnActorAsJson(const FBlueprintSpawnParams& Params) -> TSharedPtr<FJsonObject>;

		// Component operations
		auto AddComponent(const FComponentParams& Params) -> TResult<UBlueprint*>;

		auto AddComponentAsJson(const FComponentParams& Params) -> TSharedPtr<FJsonObject>;

		// Property operations
		auto SetComponentProperty(
			const FString& BlueprintName,
			const FString& ComponentName,
			const FPropertyParams& PropertyParams
		) -> FVoidResult;

		auto SetComponentPropertyAsJson(
			const FString& BlueprintName,
			const FString& ComponentName,
			const FPropertyParams& PropertyParams
		) -> TSharedPtr<FJsonObject>;

		// Physics operations
		auto SetPhysicsProperties(const FPhysicsParams& Params) -> FVoidResult;

		auto SetPhysicsPropertiesAsJson(const FPhysicsParams& Params) -> TSharedPtr<FJsonObject>;

		// Blueprint property operations
		auto SetBlueprintProperty(const FString& BlueprintName, const FPropertyParams& PropertyParams) -> FVoidResult;

		auto SetBlueprintPropertyAsJson(
			const FString& BlueprintName,
			const FPropertyParams& PropertyParams
		) -> TSharedPtr<FJsonObject>;

	private:
		/** Helper to convert AActor* to JSON */
		auto ActorToJson(AActor* Actor, bool bDetailed = true) const -> TSharedPtr<FJsonObject>;

		/** Helper to create error JSON response */
		auto CreateErrorResponse(const FString& Error) const -> TSharedPtr<FJsonObject>;

		/** Helper to create success JSON response */
		auto CreateSuccessResponse(const TSharedPtr<FJsonObject>& Data = nullptr) const -> TSharedPtr<FJsonObject>;
	};
}
