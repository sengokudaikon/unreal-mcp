#include "Commands/BlueprintNode/AddBlueprintVariable.h"
#include "Commands/CommonUtils.h"
#include "Engine/Blueprint.h"
#include "EdGraphSchema_K2.h"
#include "Kismet2/BlueprintEditorUtils.h"

auto FAddBlueprintVariable::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// Get required parameters
	FString BlueprintName;
	if (!Params->TryGetStringField(TEXT("blueprint_name"), BlueprintName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'blueprint_name' parameter"));
	}

	FString VariableName;
	if (!Params->TryGetStringField(TEXT("variable_name"), VariableName)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'variable_name' parameter"));
	}

	FString VariableType;
	if (!Params->TryGetStringField(TEXT("variable_type"), VariableType)) {
		return FCommonUtils::CreateErrorResponse(TEXT("Missing 'variable_type' parameter"));
	}

	// Get optional parameters
	bool IsExposed = false;
	if (Params->HasField(TEXT("is_exposed"))) {
		IsExposed = Params->GetBoolField(TEXT("is_exposed"));
	}

	// Find the blueprint
	UBlueprint* Blueprint = FCommonUtils::FindBlueprint(BlueprintName);
	if (!Blueprint) {
		return FCommonUtils::CreateErrorResponse(
			FString::Printf(TEXT("Blueprint not found: %s"), *BlueprintName));
	}

	// Create variable based on type
	FEdGraphPinType PinType;

	// Set up pin type based on variable_type string
	if (VariableType == TEXT("Boolean")) {
		PinType.PinCategory = UEdGraphSchema_K2::PC_Boolean;
	}
	else if (VariableType == TEXT("Integer") || VariableType == TEXT("Int")) {
		PinType.PinCategory = UEdGraphSchema_K2::PC_Int;
	}
	else if (VariableType == TEXT("Float")) {
		PinType.PinCategory = UEdGraphSchema_K2::PC_Float;
	}
	else if (VariableType == TEXT("String")) {
		PinType.PinCategory = UEdGraphSchema_K2::PC_String;
	}
	else if (VariableType == TEXT("Vector")) {
		PinType.PinCategory = UEdGraphSchema_K2::PC_Struct;
		PinType.PinSubCategoryObject = TBaseStructure<FVector>::Get();
	}
	else {
		return FCommonUtils::CreateErrorResponse(
			FString::Printf(TEXT("Unsupported variable type: %s"), *VariableType));
	}

	// Create the variable
	FBlueprintEditorUtils::AddMemberVariable(Blueprint, FName(*VariableName), PinType);

	// Set variable properties
	FBPVariableDescription* NewVar = nullptr;
	for (FBPVariableDescription& Variable : Blueprint->NewVariables) {
		if (Variable.VarName == FName(*VariableName)) {
			NewVar = &Variable;
			break;
		}
	}

	if (NewVar) {
		// Set exposure in editor
		if (IsExposed) {
			NewVar->PropertyFlags |= CPF_Edit;
		}
	}

	// Mark the blueprint as modified
	FBlueprintEditorUtils::MarkBlueprintAsModified(Blueprint);

	TSharedPtr<FJsonObject> ResultObj = MakeShared<FJsonObject>();
	ResultObj->SetStringField(TEXT("variable_name"), VariableName);
	ResultObj->SetStringField(TEXT("variable_type"), VariableType);
	return ResultObj;
}
