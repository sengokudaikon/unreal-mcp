#pragma once

#include "CoreMinimal.h"
#include "Json.h"

class FUnrealMCPEnhancedInputCommands {
public:
	FUnrealMCPEnhancedInputCommands();
	~FUnrealMCPEnhancedInputCommands() = default;

	auto HandleCommand(
		const FString& CommandType,
		const TSharedPtr<FJsonObject>& Params
	) -> TSharedPtr<FJsonObject>;

private:
	using FCommandHandler = TSharedPtr<FJsonObject> (*)(const TSharedPtr<FJsonObject>&);
	TMap<FString, FCommandHandler> CommandHandlers;
};
