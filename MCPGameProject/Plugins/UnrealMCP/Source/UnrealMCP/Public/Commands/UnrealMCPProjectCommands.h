#pragma once

#include "CoreMinimal.h"
#include "Json.h"

/**
 * Handler class for Project-wide MCP commands
 */
class UNREALMCP_API FUnrealMCPProjectCommands {
public:
	FUnrealMCPProjectCommands();

	// Handle project commands
	TSharedPtr<FJsonObject> HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params);

private:
	// Legacy input command handlers
	static TSharedPtr<FJsonObject> HandleCreateInputMapping(const TSharedPtr<FJsonObject>& Params);
};
