#include "Commands/Input/ClearAllMappingContexts.h"
#include "Commands/CommonUtils.h"
#include "Services/InputService.h"
#include "Core/MCPTypes.h"

auto FClearAllMappingContexts::Handle(
	const TSharedPtr<FJsonObject>& Params
) -> TSharedPtr<FJsonObject> {
	// No parameter parsing needed for this command

	// Delegate to service
	UnrealMCP::FVoidResult Result =
		UnrealMCP::FInputService::ClearAllMappingContexts();

	if (Result.IsFailure()) {
		return FCommonUtils::CreateErrorResponse(Result.GetError());
	}

	// Build JSON response
	TSharedPtr<FJsonObject> Response = MakeShared<FJsonObject>();
	Response->SetBoolField(TEXT("success"), true);
	return Response;
}
