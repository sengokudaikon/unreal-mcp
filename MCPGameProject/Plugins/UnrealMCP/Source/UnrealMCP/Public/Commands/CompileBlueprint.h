#pragma once

#include "CoreMinimal.h"

class UNREALMCP_API FCompileBlueprint {
public:
	FCompileBlueprint() = default;

	~FCompileBlueprint() = default;

	static auto Handle(const TSharedPtr<FJsonObject>& Params) -> TSharedPtr<FJsonObject>;
};
