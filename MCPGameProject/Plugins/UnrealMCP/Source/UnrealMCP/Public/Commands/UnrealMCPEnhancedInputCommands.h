#pragma once

#include "CoreMinimal.h"
#include "JsonObject.h"

class FUnrealMCPEnhancedInputCommands {
public:
	FUnrealMCPEnhancedInputCommands() = default;

	~FUnrealMCPEnhancedInputCommands() = default;

	static auto HandleCommand(
		const FString& CommandType,
		const TSharedPtr<FJsonObject>& Params
	) -> TSharedPtr<FJsonObject>;

private:
	// Enhanced Input command handlers
	static auto HandleCreateEnhancedInputAction(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleCreateInputMappingContext(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleAddEnhancedInputMapping(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleRemoveEnhancedInputMapping(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleApplyMappingContext(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleRemoveMappingContext(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;

	static auto HandleClearAllMappingContexts(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;
};
