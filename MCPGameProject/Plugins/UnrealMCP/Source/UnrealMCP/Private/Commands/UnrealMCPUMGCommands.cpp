#include "Commands/UnrealMCPUMGCommands.h"
#include "Commands/CommonUtils.h"
#include "Services/WidgetService.h"
#include "Core/MCPTypes.h"
#include "WidgetBlueprint.h"

FUnrealMCPUMGCommands::FUnrealMCPUMGCommands()
{
}

auto FUnrealMCPUMGCommands::HandleCommand(
	const FString& CommandName,
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	if (CommandName == TEXT("create_umg_widget_blueprint"))
	{
		return HandleCreateUMGWidgetBlueprint(Params);
	}
	if (CommandName == TEXT("add_text_block_to_widget"))
	{
		return HandleAddTextBlockToWidget(Params);
	}
	if (CommandName == TEXT("add_widget_to_viewport"))
	{
		return HandleAddWidgetToViewport(Params);
	}
	if (CommandName == TEXT("add_button_to_widget"))
	{
		return HandleAddButtonToWidget(Params);
	}
	if (CommandName == TEXT("bind_widget_event"))
	{
		return HandleBindWidgetEvent(Params);
	}
	if (CommandName == TEXT("set_text_block_binding"))
	{
		return HandleSetTextBlockBinding(Params);
	}

	return FCommonUtils::CreateErrorResponse(
		FString::Printf(TEXT("Unknown UMG command: %s"), *CommandName)
	);
}

auto FUnrealMCPUMGCommands::HandleCreateUMGWidgetBlueprint(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FWidgetCreationParams> ParamsResult =
		UnrealMCP::FWidgetCreationParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::TResult<UWidgetBlueprint*> Result =
		UnrealMCP::FWidgetService::CreateWidget(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FWidgetCreationParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("name"), ParsedParams.Name);
	Response->SetStringField(TEXT("path"), ParsedParams.PackagePath / ParsedParams.Name);
	return Response;
}

auto FUnrealMCPUMGCommands::HandleAddTextBlockToWidget(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FTextBlockParams> ParamsResult =
		UnrealMCP::FTextBlockParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::TResult<UTextBlock*> Result =
		UnrealMCP::FWidgetService::AddTextBlock(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FTextBlockParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("widget_name"), ParsedParams.TextBlockName);
	Response->SetStringField(TEXT("text"), ParsedParams.Text);
	return Response;
}

auto FUnrealMCPUMGCommands::HandleAddButtonToWidget(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FButtonParams> ParamsResult =
		UnrealMCP::FButtonParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::TResult<UButton*> Result =
		UnrealMCP::FWidgetService::AddButton(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FButtonParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("widget_name"), ParsedParams.ButtonName);
	Response->SetStringField(TEXT("text"), ParsedParams.Text);
	return Response;
}

auto FUnrealMCPUMGCommands::HandleBindWidgetEvent(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FWidgetEventBindingParams> ParamsResult =
		UnrealMCP::FWidgetEventBindingParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::FVoidResult Result =
		UnrealMCP::FWidgetService::BindWidgetEvent(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FWidgetEventBindingParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("widget_component_name"), ParsedParams.WidgetComponentName);
	Response->SetStringField(TEXT("event_name"), ParsedParams.EventName);
	return Response;
}

auto FUnrealMCPUMGCommands::HandleSetTextBlockBinding(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FTextBlockBindingParams> ParamsResult =
		UnrealMCP::FTextBlockBindingParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::FVoidResult Result =
		UnrealMCP::FWidgetService::SetTextBlockBinding(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FTextBlockBindingParams& ParsedParams = ParamsResult.GetValue();
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("text_block_name"), ParsedParams.TextBlockName);
	Response->SetStringField(TEXT("binding_property"), ParsedParams.BindingProperty);
	return Response;
}

auto FUnrealMCPUMGCommands::HandleAddWidgetToViewport(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject>
{
	// Parse JSON to params struct
	UnrealMCP::TResult<UnrealMCP::FAddWidgetToViewportParams> ParamsResult =
		UnrealMCP::FAddWidgetToViewportParams::FromJson(Params);

	if (ParamsResult.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(ParamsResult.GetError());
	}

	// Delegate to service
	UnrealMCP::TResult<UClass*> Result =
		UnrealMCP::FWidgetService::GetWidgetClass(ParamsResult.GetValue());

	if (Result.IsFailure())
	{
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	const UnrealMCP::FAddWidgetToViewportParams& ParsedParams = ParamsResult.GetValue();
	UClass* WidgetClass = Result.GetValue();

	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetStringField(TEXT("widget_name"), ParsedParams.WidgetName);
	Response->SetStringField(TEXT("class_path"), WidgetClass ? WidgetClass->GetPathName() : TEXT(""));
	Response->SetNumberField(TEXT("z_order"), ParsedParams.ZOrder);
	Response->SetStringField(
		TEXT("note"),
		TEXT("Widget class ready. Use CreateWidget and AddToViewport nodes in Blueprint to display in game.")
	);
	return Response;
}
