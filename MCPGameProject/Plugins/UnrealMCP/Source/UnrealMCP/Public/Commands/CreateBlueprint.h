#pragma once

#include "CoreMinimal.h"
#include "Json.h"

class UNREALMCP_API FCreateBlueprint {
public:
	FCreateBlueprint() = default;
	~FCreateBlueprint() = default;

	static auto Handle(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;
};