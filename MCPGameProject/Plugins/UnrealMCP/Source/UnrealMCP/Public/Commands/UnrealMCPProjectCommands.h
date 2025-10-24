#pragma once

#include "CoreMinimal.h"
#include "Json.h"

/**
 * Handler class for Project-wide MCP commands
 */
class UNREALMCP_API FUnrealMCPProjectCommands
{
public:
    FUnrealMCPProjectCommands();

    // Handle project commands
    TSharedPtr<FJsonObject> HandleCommand(const FString& CommandType, const TSharedPtr<FJsonObject>& Params);

private:
    // Legacy input command handlers
    TSharedPtr<FJsonObject> HandleCreateInputMapping(const TSharedPtr<FJsonObject>& Params);

    // Enhanced Input command handlers
    TSharedPtr<FJsonObject> HandleCreateEnhancedInputAction(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleCreateInputMappingContext(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleAddEnhancedInputMapping(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleRemoveEnhancedInputMapping(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleApplyMappingContext(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleRemoveMappingContext(const TSharedPtr<FJsonObject>& Params);
    TSharedPtr<FJsonObject> HandleClearAllMappingContexts(const TSharedPtr<FJsonObject>& Params);
}; 