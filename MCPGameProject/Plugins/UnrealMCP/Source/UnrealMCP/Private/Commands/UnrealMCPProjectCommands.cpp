#include "Commands/UnrealMCPProjectCommands.h"
#include "Commands/CommonUtils.h"
#include "GameFramework/InputSettings.h"

FUnrealMCPProjectCommands::FUnrealMCPProjectCommands() {
}

TSharedPtr<FJsonObject> FUnrealMCPProjectCommands::HandleCommand(const FString& CommandType,
                                                                 const TSharedPtr<FJsonObject>& Params) {
	// Legacy input commands
	if (CommandType == TEXT("create_input_mapping")) {
		return HandleCreateInputMapping(Params);
	}

	return FCommonUtils::CreateErrorResponse(
		FString::Printf(TEXT("Unknown project command: %s"), *CommandType));
}

auto FUnrealMCPProjectCommands::HandleCreateInputMapping(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Get required parameters
	FString ActionName;
	if (!Params->TryGetStringField(TEXT("action_name"), ActionName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'action_name' parameter"));
	}

	FString Key;
	if (!Params->TryGetStringField(TEXT("key"), Key)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'key' parameter"));
	}

	// Get the input settings
	UInputSettings* InputSettings = GetMutableDefault<UInputSettings>();
	if (!InputSettings) {
		return FCommonUtils::CreateErrorResponse(TEXT("Failed to get input settings"));
	}

	// Create the input action mapping
	FInputActionKeyMapping ActionMapping;
	ActionMapping.ActionName = FName(*ActionName);
	ActionMapping.Key = FKey(*Key);

	// Add modifiers if provided
	if (Params->HasField(TEXT("shift"))) {
		ActionMapping.bShift = Params->GetBoolField(TEXT("shift"));
	}
	if (Params->HasField(TEXT("ctrl"))) {
		ActionMapping.bCtrl = Params->GetBoolField(TEXT("ctrl"));
	}
	if (Params->HasField(TEXT("alt"))) {
		ActionMapping.bAlt = Params->GetBoolField(TEXT("alt"));
	}
	if (Params->HasField(TEXT("cmd"))) {
		ActionMapping.bCmd = Params->GetBoolField(TEXT("cmd"));
	}

	// Add the mapping
	InputSettings->AddActionMapping(ActionMapping);
	InputSettings->SaveConfig();

	TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
	ResultObj->SetStringField(TEXT("action_name"), ActionName);
	ResultObj->SetStringField(TEXT("key"), Key);
	return ResultObj;
}

