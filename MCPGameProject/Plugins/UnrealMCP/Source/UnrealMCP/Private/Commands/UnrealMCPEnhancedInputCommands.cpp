#include "Commands/UnrealMCPEnhancedInputCommands.h"

#include "Commands/Input/CreateEnhancedInputAction.h"
#include "Commands/Input/CreateInputMappingContext.h"
#include "Commands/Input/AddEnhancedInputMapping.h"
#include "Commands/Input/RemoveEnhancedInputMapping.h"
#include "Commands/Input/ApplyMappingContext.h"
#include "Commands/Input/RemoveMappingContext.h"
#include "Commands/Input/ClearAllMappingContexts.h"
#include "Commands/CommonUtils.h"

FUnrealMCPEnhancedInputCommands::FUnrealMCPEnhancedInputCommands() {
	CommandHandlers.Add(TEXT("create_enhanced_input_action"), &FCreateEnhancedInputAction::Handle);
	CommandHandlers.Add(TEXT("create_input_mapping_context"), &FCreateInputMappingContext::Handle);
	CommandHandlers.Add(TEXT("add_enhanced_input_mapping"), &FAddEnhancedInputMapping::Handle);
	CommandHandlers.Add(TEXT("remove_enhanced_input_mapping"), &FRemoveEnhancedInputMapping::Handle);
	CommandHandlers.Add(TEXT("apply_mapping_context"), &FApplyMappingContext::Handle);
	CommandHandlers.Add(TEXT("remove_mapping_context"), &FRemoveMappingContext::Handle);
	CommandHandlers.Add(TEXT("clear_all_mapping_contexts"), &FClearAllMappingContexts::Handle);
}

TSharedPtr<FJsonObject> FUnrealMCPEnhancedInputCommands::HandleCommand(
	const FString& CommandType,
	const TSharedPtr<FJsonObject>& Params
) {
	if (const auto* Handler = CommandHandlers.Find(CommandType)) {
		return (*Handler)(Params);
	}

	return FCommonUtils::CreateErrorResponse(FString::Printf(TEXT("Unknown enhanced input command: %s"), *CommandType));
}
