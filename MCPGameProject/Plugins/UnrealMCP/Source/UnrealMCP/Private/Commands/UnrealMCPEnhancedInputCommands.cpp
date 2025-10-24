#include "Commands/UnrealMCPEnhancedInputCommands.h"
#include "Commands/CommonUtils.h"
#include "Services/InputService.h"
#include "Core/MCPTypes.h"

auto FUnrealMCPEnhancedInputCommands::HandleCommand(
	const FString& CommandType,
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	if (CommandType == TEXT("create_enhanced_input_action"))
	{
		return HandleCreateEnhancedInputAction(Params);
	}
	if (CommandType == TEXT("create_input_mapping_context"))
	{
		return HandleCreateInputMappingContext(Params);
	}
	if (CommandType == TEXT("add_enhanced_input_mapping"))
	{
		return HandleAddEnhancedInputMapping(Params);
	}
	if (CommandType == TEXT("remove_enhanced_input_mapping"))
	{
		return HandleRemoveEnhancedInputMapping(Params);
	}
	if (CommandType == TEXT("apply_mapping_context"))
	{
		return HandleApplyMappingContext(Params);
	}
	if (CommandType == TEXT("remove_mapping_context"))
	{
		return HandleRemoveMappingContext(Params);
	}
	if (CommandType == TEXT("clear_all_mapping_contexts"))
	{
		return HandleClearAllMappingContexts(Params);
	}

	return FCommonUtils::CreateErrorResponse(
		FString::Printf(TEXT("Unknown enhanced input command: %s"), *CommandType)
	);
}

auto FUnrealMCPEnhancedInputCommands::HandleCreateEnhancedInputAction(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FInputActionParams> ParamsResult =
		UnrealMCP::FInputActionParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::TResult<UInputAction*> Result =
		UnrealMCP::FInputService::CreateInputAction(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FInputActionParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("name"), ParsedParams.Name);
	Response->SetStringField(TEXT("value_type"), ParsedParams.ValueType);
	Response->SetStringField(
		TEXT("asset_path"),
		ParsedParams.Path / FString::Printf(TEXT("IA_%s"), *ParsedParams.Name)
	);
	return Response;
}

auto FUnrealMCPEnhancedInputCommands::HandleCreateInputMappingContext(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FInputMappingContextParams> ParamsResult =
		UnrealMCP::FInputMappingContextParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::TResult<UInputMappingContext*> Result =
		UnrealMCP::FInputService::CreateInputMappingContext(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FInputMappingContextParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("name"), ParsedParams.Name);
	Response->SetStringField(
		TEXT("asset_path"),
		ParsedParams.Path / FString::Printf(TEXT("IMC_%s"), *ParsedParams.Name)
	);
	return Response;
}

auto FUnrealMCPEnhancedInputCommands::HandleAddEnhancedInputMapping(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FAddMappingParams> ParamsResult =
		UnrealMCP::FAddMappingParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::FVoidResult Result =
		UnrealMCP::FInputService::AddMappingToContext(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FAddMappingParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("context_path"), ParsedParams.ContextPath);
	Response->SetStringField(TEXT("action_path"), ParsedParams.ActionPath);
	Response->SetStringField(TEXT("key"), ParsedParams.Key);
	return Response;
}

auto FUnrealMCPEnhancedInputCommands::HandleRemoveEnhancedInputMapping(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FAddMappingParams> ParamsResult =
		UnrealMCP::FAddMappingParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::FVoidResult Result =
		UnrealMCP::FInputService::RemoveMappingFromContext(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FAddMappingParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("context_path"), ParsedParams.ContextPath);
	Response->SetStringField(TEXT("action_path"), ParsedParams.ActionPath);
	return Response;
}

auto FUnrealMCPEnhancedInputCommands::HandleApplyMappingContext(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// TODO: Move to a dedicated runtime input service (this is not editor-time asset management)
	return FCommonUtils::CreateErrorResponse(
		TEXT("apply_mapping_context is not yet implemented - requires runtime input service")
	);
}

auto FUnrealMCPEnhancedInputCommands::HandleRemoveMappingContext(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// TODO: Move to a dedicated runtime input service (this is not editor-time asset management)
	return FCommonUtils::CreateErrorResponse(
		TEXT("remove_mapping_context is not yet implemented - requires runtime input service")
	);
}

auto FUnrealMCPEnhancedInputCommands::HandleClearAllMappingContexts(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// TODO: Move to a dedicated runtime input service (this is not editor-time asset management)
	return FCommonUtils::CreateErrorResponse(
		TEXT("clear_all_mapping_contexts is not yet implemented - requires runtime input service")
	);
}
