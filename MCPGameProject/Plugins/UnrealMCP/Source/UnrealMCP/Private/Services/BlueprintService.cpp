#include "Services/BlueprintService.h"
#include "Factories/BlueprintActorFactory.h"
#include "Commands/UnrealMCPCommonUtils.h"
#include "Engine/Blueprint.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "Editor.h"

namespace UnrealMCP
{
	TResult<AActor*> FBlueprintService::SpawnActor(const FBlueprintSpawnParams& Params)
	{
		// Find the blueprint
		UBlueprint* Blueprint = FUnrealMCPCommonUtils::FindBlueprint(Params.BlueprintName);
		if (!Blueprint)
		{
			return TResult<AActor*>::Failure(
				FString::Printf(TEXT("Blueprint not found: %s"), *Params.BlueprintName)
			);
		}

		// Get the world context
		UWorld* World = GEditor->GetEditorWorldContext().World();
		if (!World)
		{
			return TResult<AActor*>::Failure(TEXT("Failed to get editor world"));
		}

		// Build transform
		FTransform SpawnTransform;
		SpawnTransform.SetLocation(Params.Location.Get(FVector::ZeroVector));
		SpawnTransform.SetRotation(FQuat(Params.Rotation.Get(FRotator::ZeroRotator)));

		// Use factory to spawn
		return FBlueprintActorFactory::SpawnFromBlueprint(
			Blueprint,
			Params.ActorName,
			SpawnTransform,
			World
		);
	}

	TSharedPtr<FJsonObject> FBlueprintService::SpawnActorAsJson(const FBlueprintSpawnParams& Params)
	{
		TResult<AActor*> Result = SpawnActor(Params);

		if (Result.IsSuccess())
		{
			return ActorToJson(Result.GetValue(), true);
		}

		return CreateErrorResponse(Result.GetError());
	}

	TResult<UBlueprint*> FBlueprintService::AddComponent(const FComponentParams& Params)
	{
		// Find the blueprint
		UBlueprint* Blueprint = FUnrealMCPCommonUtils::FindBlueprint(Params.BlueprintName);
		if (!Blueprint)
		{
			return TResult<UBlueprint*>::Failure(
				FString::Printf(TEXT("Blueprint not found: %s"), *Params.BlueprintName)
			);
		}

		// TODO: Implement component adding logic
		// For now, return a placeholder
		return TResult<UBlueprint*>::Failure(TEXT("AddComponent not yet fully implemented in service"));
	}

	TSharedPtr<FJsonObject> FBlueprintService::AddComponentAsJson(const FComponentParams& Params)
	{
		TResult<UBlueprint*> Result = AddComponent(Params);

		if (Result.IsSuccess())
		{
			TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
			Response->SetStringField(TEXT("blueprint_name"), Params.BlueprintName);
			Response->SetStringField(TEXT("component_name"), Params.ComponentName);
			Response->SetStringField(TEXT("component_type"), Params.ComponentType);
			Response->SetBoolField(TEXT("success"), true);
			return Response;
		}

		return CreateErrorResponse(Result.GetError());
	}

	FVoidResult FBlueprintService::SetComponentProperty(
		const FString& BlueprintName,
		const FString& ComponentName,
		const FPropertyParams& PropertyParams)
	{
		// TODO: Implement
		return FVoidResult::Failure(TEXT("SetComponentProperty not yet implemented in service"));
	}

	TSharedPtr<FJsonObject> FBlueprintService::SetComponentPropertyAsJson(
		const FString& BlueprintName,
		const FString& ComponentName,
		const FPropertyParams& PropertyParams)
	{
		FVoidResult Result = SetComponentProperty(BlueprintName, ComponentName, PropertyParams);

		if (Result.IsSuccess())
		{
			TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
			Response->SetStringField(TEXT("component"), ComponentName);
			Response->SetStringField(TEXT("property"), PropertyParams.PropertyName);
			Response->SetBoolField(TEXT("success"), true);
			return Response;
		}

		return CreateErrorResponse(Result.GetError());
	}

	FVoidResult FBlueprintService::SetPhysicsProperties(const FPhysicsParams& Params)
	{
		// TODO: Implement
		return FVoidResult::Failure(TEXT("SetPhysicsProperties not yet implemented in service"));
	}

	TSharedPtr<FJsonObject> FBlueprintService::SetPhysicsPropertiesAsJson(const FPhysicsParams& Params)
	{
		FVoidResult Result = SetPhysicsProperties(Params);

		if (Result.IsSuccess())
		{
			TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
			Response->SetStringField(TEXT("component"), Params.ComponentName);
			Response->SetBoolField(TEXT("success"), true);
			return Response;
		}

		return CreateErrorResponse(Result.GetError());
	}

	FVoidResult FBlueprintService::SetBlueprintProperty(
		const FString& BlueprintName,
		const FPropertyParams& PropertyParams)
	{
		// TODO: Implement
		return FVoidResult::Failure(TEXT("SetBlueprintProperty not yet implemented in service"));
	}

	TSharedPtr<FJsonObject> FBlueprintService::SetBlueprintPropertyAsJson(
		const FString& BlueprintName,
		const FPropertyParams& PropertyParams)
	{
		FVoidResult Result = SetBlueprintProperty(BlueprintName, PropertyParams);

		if (Result.IsSuccess())
		{
			TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
			Response->SetStringField(TEXT("property"), PropertyParams.PropertyName);
			Response->SetBoolField(TEXT("success"), true);
			return Response;
		}

		return CreateErrorResponse(Result.GetError());
	}

	// Helper methods

	TSharedPtr<FJsonObject> FBlueprintService::ActorToJson(AActor* Actor, bool bDetailed) const
	{
		return FUnrealMCPCommonUtils::ActorToJsonObject(Actor, bDetailed);
	}

	TSharedPtr<FJsonObject> FBlueprintService::CreateErrorResponse(const FString& Error) const
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(Error);
	}

	TSharedPtr<FJsonObject> FBlueprintService::CreateSuccessResponse(const TSharedPtr<FJsonObject>& Data) const
	{
		return FUnrealMCPCommonUtils::CreateSuccessResponse(Data);
	}
}
