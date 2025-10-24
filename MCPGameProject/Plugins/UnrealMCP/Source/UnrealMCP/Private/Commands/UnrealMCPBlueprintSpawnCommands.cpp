#include "Commands/UnrealMCPBlueprintSpawnCommands.h"
#include "Services/BlueprintService.h"
#include "Core/MCPTypes.h"
#include "Commands/UnrealMCPCommonUtils.h"

FUnrealMCPBlueprintSpawnCommands::FUnrealMCPBlueprintSpawnCommands()
{
}

TSharedPtr<FJsonObject> FUnrealMCPBlueprintSpawnCommands::HandleSpawnBlueprintActor(
	const TSharedPtr<FJsonObject>& Params)
{
	// Parse JSON into typed parameters
	UnrealMCP::TResult<UnrealMCP::FBlueprintSpawnParams> ParamsResult =
		UnrealMCP::FBlueprintSpawnParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FUnrealMCPCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	return GetService()->SpawnActorAsJson(ParamsResult.GetValue());
}

TSharedPtr<UnrealMCP::FBlueprintService> FUnrealMCPBlueprintSpawnCommands::GetService()
{
	// Use a static instance for now (could be injected in the future)
	static TSharedPtr<UnrealMCP::FBlueprintService> Service = MakeShared<UnrealMCP::FBlueprintService>();
	return Service;
}
