# Header
## sub header
### topic
`test file`
## Adding HTML as sample
`#!/usr/bin/env bash
set -e

REPO_DIR="many-branches-advanced"
BRANCH_COUNT=80
max_commits=5

rm -rf "$REPO_DIR"
mkdir "$REPO_DIR"
cd "$REPO_DIR"

git init -b main

# initial commit
echo "# Many Branches Repo" > README.md
git add README.md
git commit -m "Initial commit: README"

# helper to random integer
rand() {
  shuf -i "$1"-"$2" -n1
}

for i in $(seq 1 $BRANCH_COUNT); do
  branch="feature/issue-$i"
  git checkout -b "$branch" main

  commits=$(rand 1 $max_commits)
  for c in $(seq 1 $commits); do
    file="f${i}_${c}.txt"
    echo "branch $branch commit $c" >> "$file"
    echo "timestamp: $(date --iso-8601=seconds)" >> "$file"
    git add "$file"
    git commit -m "[$branch] commit $c"
  done

  # occasionally tag a commit on the branch
  if [ $((i % 10)) -eq 0 ]; then
    git tag -a "tag-$i" -m "Tag on $branch"
  fi
done

# merge some branches back to main using --no-ff to create merge commits
git checkout main
for j in 1 5 10 20 50; do
  b="feature/issue-$j"
  if git show-ref --verify --quiet "refs/heads/$b"; then
    git merge --no-ff -m "Merge $b into main (demo)" "$b" || git merge --abort
  fi
done

# list branches and tag summary
echo "Done. Branch count: $(git branch --list | wc -l)"
git branch --list
git tag --list


# Unreal code
## Files to add

### Create two files in your UE project's Source/<YourProject>/ folder.

`FlyingPawn.h`

// FlyingPawn.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "FlyingPawn.generated.h"

UCLASS()
class YOURPROJECT_API AFlyingPawn : public APawn
{
    GENERATED_BODY()

public:
    AFlyingPawn();

    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;
    virtual void BeginPlay() override;

protected:
    // Components
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UStaticMeshComponent* BodyMesh;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    USceneComponent* Root;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    UCameraComponent* Camera;

    // Flight state
    FVector Velocity;
    float Throttle;        // 0..1
    float CurrentSpeed;    // m/s

    // Control inputs (-1..1)
    float PitchInput;
    float RollInput;
    float YawInput;

    // Configurable properties
    UPROPERTY(EditAnywhere, Category = "Flight|Physics")
    float Mass;

    UPROPERTY(EditAnywhere, Category = "Flight|Physics", meta = (ClampMin = "0.1"))
    float WingArea;        // m^2

    UPROPERTY(EditAnywhere, Category = "Flight|Physics")
    float MaxThrust;      // Newtons at full throttle

    UPROPERTY(EditAnywhere, Category = "Flight|Physics")
    float LiftCoefficient; // CL (approx)

    UPROPERTY(EditAnywhere, Category = "Flight|Physics")
    float DragCoefficient; // CD (parasitic + induced)

    UPROPERTY(EditAnywhere, Category = "Flight|Controls")
    float PitchRate;      // degrees/sec per input unit

    UPROPERTY(EditAnywhere, Category = "Flight|Controls")
    float RollRate;       // degrees/sec per input unit

    UPROPERTY(EditAnywhere, Category = "Flight|Controls")
    float YawRate;        // degrees/sec per input unit

    UPROPERTY(EditAnywhere, Category = "Flight|FlightModel")
    float AirDensity;     // kg/m^3 (1.225 at sea level)

    UPROPERTY(EditAnywhere, Category = "Flight|FlightModel")
    float StallSpeed;     // m/s - below this stall occurs

    UPROPERTY(EditAnywhere, Category = "Flight|FlightModel")
    float MaxBankAngle;   // degrees

    // Helpers
    void ApplyPhysics(float DeltaTime);
    FVector CalculateLift(float DeltaTime);
    float CalculateDragMagnitude() const;
    void UpdateRotationFromControls(float DeltaTime);

    // Input callbacks
    void MovePitch(float Value);
    void MoveRoll(float Value);
    void MoveYaw(float Value);
    void ThrottleUp(float Value);
};

# How to integrate into your Unreal project

## Replace YOURPROJECT_API
In FlyingPawn.h replace YOURPROJECT_API with your module macro (usually the name of your project in caps followed by _API). For quick testing you can also remove it (but it’s needed for packaging).

Add the files to your project
Put FlyingPawn.h and FlyingPawn.cpp under Source/<YourProject>/ and regenerate project files (right-click .uproject → Generate Visual Studio / Xcode project files). Then compile.

Input bindings
Open Edit → Project Settings → Input and add following Axis Mappings:

Axis Pitch → bind to Mouse Y (scale -1) and/or Gamepad Right Y

Axis Roll → bind to A/D or Gamepad Right X

Axis Yaw → bind to Q/E or Gamepad Left X

Axis Throttle → bind to Mouse Wheel or Gamepad Trigger (ensure range 0..1)
Example: Throttle with W scale 1 and S scale 0 may also work if you prefer on/off.

For precise throttle control, you can map Throttle to an axis that returns 0..1 (or adapt code to map -1..1 to 0..1).

Place the pawn in the level
In UE Editor, add the AFlyingPawn as a Blueprint subclass (optional) or drag the C++ class into the world. In World Settings set GameMode to a GameMode that uses this pawn (or set Auto Possess Player = Player0 as in the code).

Tuning
The flight model is intentionally simple. Tune these values in the Details panel at runtime:

Mass, WingArea, LiftCoefficient, DragCoefficient, MaxThrust

StallSpeed and control rates

Units & notes

This code uses approximate SI units (meters/second/kg/Newtons) but Unreal uses centimeters internally. Values are chosen to be reasonable; you may need to scale or convert if you want exact realism.

Gravity used as 9.81 m/s² and thrust in Newtons. If you want to match Unreal's cm units exactly, multiply positions/velocity by 100 and adjust constants accordingly.

Enhancements you can add

Propulsion curve: make thrust vary with airspeed or altitude.

Induced drag: add drag term proportional to lift².

Control surfaces: simulate ailerons/rudder with differential lift.

G-loading / structural limits: limit maximum pitch/roll rates based on airspeed.

Ground collision & landing gear: add wheels + suspension.

Wind & turbulence: add noise forces and gusts.

HUD: show airspeed, altitude, pitch/roll indicators.

PID autopilot: for steady heading/altitude hold.

If you want, I can:

Convert this into a ready-to-import Blueprintable component or MovementComponent,

Add a fully unit-consistent version using Unreal's cm units,

Implement a more realistic aerodynamic model (lift curve vs AoA, induced drag, control surface effectiveness),

Or produce a sample Unreal plugin that includes assets and an in-editor tuning UI.

1. buoyancy (based on immersion depth)

2. swimming thrust (forward/back/strafe + ascend/descend)

3. water drag

4. simple water current

5. sprinting / dash

6. oxygen / drowning system

7. simple surface behavior (breath refill)

8. hooks for animations / VFX

Save two files under `Source/<YourProject>/`: `UnderwaterPawn.h` and `UnderwaterPawn.cpp.` Replace `YOURPROJECT_API` with your module API macro (or remove for quick tests).

## UnderwaterPawn.h
// UnderwaterPawn.h
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "UnderwaterPawn.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnOxygenChanged, float, NewOxygenPercent);
DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnDrowned);

UCLASS()
class YOURPROJECT_API AUnderwaterPawn : public APawn
{
    GENERATED_BODY()

public:
    AUnderwaterPawn();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaTime) override;
    virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

    // Events
    UPROPERTY(BlueprintAssignable, Category="Underwater|Events")
    FOnOxygenChanged OnOxygenChanged;

    UPROPERTY(BlueprintAssignable, Category="Underwater|Events")
    FOnDrowned OnDrowned;

protected:
    // Components
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
    USceneComponent* Root;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
    UStaticMeshComponent* BodyMesh;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Components")
    UCameraComponent* Camera;

    // Physics state (Unreal uses cm/s; we will treat values in cm & g/cm^3 where needed)
    FVector Velocity;

    // Control inputs (-1..1)
    float ForwardInput;
    float RightInput;
    float UpInput;       // ascend/descend
    bool bSprint;

    // Configurable properties
    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    float Mass; // kg

    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    float WaterLevelZ; // world Z of water surface (cm)

    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    float BuoyancyCoefficient; // how strong buoyant force per submerged depth (N per cm approx)

    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    float WaterDensity; // kg/m^3 (1.0-ish for fresh water) -- used for reference

    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    float SwimThrust; // Newtons at full input (forward)

    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    float StrafeThrust; // Newtons for strafe

    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    float VerticalThrust; // Newtons for ascend/descend

    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    float DragCoefficient; // higher -> stronger drag in water

    UPROPERTY(EditAnywhere, Category="Underwater|Physics")
    FVector WaterCurrent; // world-space current velocity (cm/s)

    // Oxygen system
    UPROPERTY(EditAnywhere, Category="Underwater|Oxygen")
    float MaxOxygenSeconds;

    UPROPERTY(VisibleAnywhere, Category="Underwater|Oxygen")
    float CurrentOxygenSeconds;

    UPROPERTY(EditAnywhere, Category="Underwater|Oxygen")
    float OxygenDepletionRateMultiplier; // multiplier to depletion when sprinting

    UPROPERTY(EditAnywhere, Category="Underwater|Oxygen")
    float OxygenRecoveryRate;

    bool bIsUnderwater;
    bool bIsDrowned;

    // Helpers
    void ApplyPhysics(float DeltaTime);
    float GetSubmersionDepth() const; // positive value in cm: how deep the pawn's origin is below water surface
    FVector CalculateBuoyancy(float SubmersionDepth) const;
    FVector CalculateDrag() const;

    // Input callbacks
    void MoveForward(float Value);
    void MoveRight(float Value);
    void MoveUp(float Value); // ascend/descend
    void SprintPressed();
    void SprintReleased();

    // Drowning / oxygen
    void UpdateOxygen(float DeltaTime);
    void HandleDrown();

    // Utility
    FVector GetPawnForwardWorld() const { return GetActorForwardVector(); }
};

## UnderwaterPawn.cpp
// UnderwaterPawn.cpp
#include "UnderwaterPawn.h"
#include "Camera/CameraComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/InputComponent.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"

AUnderwaterPawn::AUnderwaterPawn()
{
    PrimaryActorTick.bCanEverTick = true;

    Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
    RootComponent = Root;

    BodyMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("BodyMesh"));
    BodyMesh->SetupAttachment(RootComponent);
    BodyMesh->SetSimulatePhysics(false); // we integrate manually
    BodyMesh->SetCollisionProfileName(TEXT("Pawn"));

    Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
    Camera->SetupAttachment(BodyMesh);
    Camera->SetRelativeLocation(FVector(-120.f, 0.f, 40.f));
    Camera->bUsePawnControlRotation = false;

    // Defaults (units: Unreal cm)
    Mass = 80.0f; // kg (human)
    WaterLevelZ = 0.0f; // world Z of water surface in cm; set in editor
    BuoyancyCoefficient = 15.0f; // tune: larger -> stronger buoyancy (N per cm)
    WaterDensity = 1000.0f; // kg/m3 (used for reference only)
    SwimThrust = 350.0f * 100.0f; // N -> convert to "stronger feel" in cm units; values tuned experimentally
    StrafeThrust = 200.0f * 100.0f;
    VerticalThrust = 250.0f * 100.0f;
    DragCoefficient = 5.0f; // large since water is viscous (tune)
    WaterCurrent = FVector(0.f, 0.f, 0.f); // cm/s

    MaxOxygenSeconds = 60.0f; // seconds underwater before drowning
    CurrentOxygenSeconds = MaxOxygenSeconds;
    OxygenDepletionRateMultiplier = 2.0f; // sprinting drains faster
    OxygenRecoveryRate = 10.0f; // seconds recovered per second at surface

    Velocity = FVector::ZeroVector;

    ForwardInput = RightInput = UpInput = 0.0f;
    bSprint = false;
    bIsUnderwater = false;
    bIsDrowned = false;

    AutoPossessPlayer = EAutoReceiveInput::Player0;
}

void AUnderwaterPawn::BeginPlay()
{
    Super::BeginPlay();
    // If your level's water surface is not at Z=0, set WaterLevelZ from world or an actor
    // Example: find an actor tagged "WaterSurface" and sample its location (left as exercise)
}

void AUnderwaterPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
    Super::SetupPlayerInputComponent(PlayerInputComponent);

    PlayerInputComponent->BindAxis(TEXT("MoveForward"), this, &AUnderwaterPawn::MoveForward);
    PlayerInputComponent->BindAxis(TEXT("MoveRight"), this, &AUnderwaterPawn::MoveRight);
    PlayerInputComponent->BindAxis(TEXT("MoveUp"), this, &AUnderwaterPawn::MoveUp);

    PlayerInputComponent->BindAction(TEXT("Sprint"), IE_Pressed, this, &AUnderwaterPawn::SprintPressed);
    PlayerInputComponent->BindAction(TEXT("Sprint"), IE_Released, this, &AUnderwaterPawn::SprintReleased);
}

void AUnderwaterPawn::Tick(float DeltaTime)
{
    Super::Tick(DeltaTime);

    if (bIsDrowned)
    {
        // simple nil behavior: zero velocity
        Velocity = FVector::ZeroVector;
        return;
    }

    // physics integration
    ApplyPhysics(DeltaTime);

    // move pawn
    FVector NewLocation = GetActorLocation() + Velocity * DeltaTime;
    SetActorLocation(NewLocation, true);

    // orientation - face movement direction if moving
    if (!Velocity.IsNearlyZero())
    {
        FRotator Target = Velocity.Rotation();
        FRotator Current = GetActorRotation();
        FRotator Smooth = FMath::RInterpTo(Current, Target, DeltaTime, 2.5f);
        SetActorRotation(Smooth);
    }

    // oxygen update: determine if submerged (origin below water)
    float SubDepth = GetSubmersionDepth();
    bIsUnderwater = (SubDepth > 5.0f); // >5cm under counts as underwater
    UpdateOxygen(DeltaTime);
}

void AUnderwaterPawn::MoveForward(float Value)
{
    ForwardInput = FMath::Clamp(Value, -1.0f, 1.0f);
}

void AUnderwaterPawn::MoveRight(float Value)
{
    RightInput = FMath::Clamp(Value, -1.0f, 1.0f);
}

void AUnderwaterPawn::MoveUp(float Value)
{
    UpInput = FMath::Clamp(Value, -1.0f, 1.0f); // ascend/descend input
}

void AUnderwaterPawn::SprintPressed()
{
    bSprint = true;
}

void AUnderwaterPawn::SprintReleased()
{
    bSprint = false;
}

float AUnderwaterPawn::GetSubmersionDepth() const
{
    // positive in cm when pawn origin is below water level
    float PawnZ = GetActorLocation().Z;
    return FMath::Max(0.0f, WaterLevelZ - PawnZ);
}

FVector AUnderwaterPawn::CalculateBuoyancy(float SubmersionDepth) const
{
    if (SubmersionDepth <= 0.0f) return FVector::ZeroVector;
    // Buoyancy force acts upward. We use a simple linear model: F_buoy = k * submergedDepth
    float BuoyMag = BuoyancyCoefficient * SubmersionDepth; // N-ish (tune)
    return FVector(0.f, 0.f, BuoyMag);
}

FVector AUnderwaterPawn::CalculateDrag() const
{
    // Drag proportional to square of relative velocity to water (in cm/s).
    FVector RelVel = Velocity - WaterCurrent;
    float Speed = RelVel.Size();
    if (Speed <= KINDA_SMALL_NUMBER) return FVector::ZeroVector;

    // Simplified drag: Fd = -Cd * v * |v|
    FVector Drag = -RelVel.GetSafeNormal() * DragCoefficient * Speed * Speed;
    return Drag;
}

void AUnderwaterPawn::ApplyPhysics(float DeltaTime)
{
    // Forces (units N). Because Unreal location uses cm, integration remains consistent if we treat acceleration = F/m (m in kg),
    // but velocities will be in cm/s. Thrust values were picked to feel good. Tune as needed.

    // Compute thrust from inputs (local space)
    FVector LocalThrust = FVector::ZeroVector;
    // forward/back
    if (FMath::Abs(ForwardInput) > KINDA_SMALL_NUMBER)
    {
        float thrust = SwimThrust * FMath::Clamp(FMath::Abs(ForwardInput), 0.0f, 1.0f);
        if (ForwardInput < 0) thrust *= 0.6f; // less reverse thrust
        LocalThrust += FVector(thrust * FMath::Sign(ForwardInput), 0.f, 0.f);
    }
    // strafe
    if (FMath::Abs(RightInput) > KINDA_SMALL_NUMBER)
    {
        float thrust = StrafeThrust * FMath::Clamp(FMath::Abs(RightInput), 0.0f, 1.0f);
        LocalThrust += FVector(0.f, thrust * FMath::Sign(RightInput), 0.f);
    }
    // vertical
    if (FMath::Abs(UpInput) > KINDA_SMALL_NUMBER)
    {
        float thrust = VerticalThrust * FMath::Clamp(FMath::Abs(UpInput), 0.0f, 1.0f);
        LocalThrust += FVector(0.f, 0.f, thrust * FMath::Sign(UpInput));
    }

    // Sprint multiplier
    float SprintMult = bSprint ? 1.6f : 1.0f;
    LocalThrust *= SprintMult;

    // Convert local thrust to world
    FVector WorldThrust = GetActorRotation().RotateVector(LocalThrust);

    // Buoyancy
    float SubDepth = GetSubmersionDepth();
    FVector Buoyancy = CalculateBuoyancy(SubDepth);

    // Gravity force (N): mass (kg) * g (m/s^2) -> convert to N (kg*m/s^2)
    // Note: our positions are cm, but physics here uses SI for force -> acceleration = F / m (m remains kg), and result is m/s^2.
    // We'll convert acceleration to cm/s^2 by *100. To avoid confusion, we use simplified approach: produce acceleration directly in cm/s^2.
    FVector Gravity = FVector(0.f, 0.f, -Mass * 980.0f); // (kg * 9.8 m/s^2) * 100 to match cm units = 980 * mass (N in cm units)

    // Drag (N-like in our units)
    FVector Drag = CalculateDrag();

    // Sum forces
    FVector TotalForces = WorldThrust + Buoyancy + Drag + Gravity;

    // Acceleration (in cm/s^2): a = F / m ; since Gravity used 980*mass we will divide by mass -> gets cm/s^2 units
    FVector Acceleration = TotalForces / Mass; // (cm/s^2)

    // Integrate velocity (cm/s)
    Velocity += Acceleration * DeltaTime;

    // Current applies as "background velocity" (we'll gently nudge toward current if idle)
    // Simple approach: add small effect of current to velocity (so actors drift)
    float CurrentInfluence = 0.5f; // tune 0..1
    Velocity = FMath::Lerp(Velocity, Velocity + WaterCurrent, CurrentInfluence * DeltaTime);

    // Damp small velocities
    if (Velocity.SizeSquared() < 1.0f) Velocity = FVector::ZeroVector;

    // Clamp speed to sane max (cm/s)
    float MaxSpeed = 2000.0f; // ~20 m/s in cm/s
    if (Velocity.Size() > MaxSpeed) Velocity = Velocity.GetSafeNormal() * MaxSpeed;
}

void AUnderwaterPawn::UpdateOxygen(float DeltaTime)
{
    if (bIsDrowned) return;

    if (bIsUnderwater)
    {
        float drain = 1.0f;
        if (bSprint) drain *= OxygenDepletionRateMultiplier;
        CurrentOxygenSeconds = FMath::Max(0.0f, CurrentOxygenSeconds - drain * DeltaTime);
        float pct = CurrentOxygenSeconds / MaxOxygenSeconds;
        OnOxygenChanged.Broadcast(pct);

        if (CurrentOxygenSeconds <= 0.0f)
        {
            HandleDrown();
        }
    }
    else
    {
        // Recover oxygen at surface
        CurrentOxygenSeconds = FMath::Min(MaxOxygenSeconds, CurrentOxygenSeconds + OxygenRecoveryRate * DeltaTime);
        OnOxygenChanged.Broadcast(CurrentOxygenSeconds / MaxOxygenSeconds);
    }
}

void AUnderwaterPawn::HandleDrown()
{
    bIsDrowned = true;
    OnDrowned.Broadcast();

    // optional: play drown animation, disable input etc.
    APlayerController* PC = Cast<APlayerController>(GetController());
    if (PC)
    {
        PC->DisableInput(PC);
    }
}

#I nput Bindings (Project Settings → Input)

### Add Axis / Action mappings:

- Axis MoveForward → W (scale +1), S (scale -1), Gamepad Left Y

- Axis MoveRight → D (1), A (-1), Gamepad Left X

- Axis MoveUp → Space (1), LeftCtrl (-1) or Gamepad face buttons / triggers

- Action Sprint → LeftShift (Pressed/Released)

### How to integrate & tune
Add files to Source/<YourProject>/, regenerate project files and compile.

Place the pawn in the level or create a Blueprint subclass for easy tweaking.

Set WaterLevelZ to match your water plane's Z in the level (in cm). Optionally, implement a water actor reference and sample surface height at the pawn's XY for waves.

Tune BuoyancyCoefficient, DragCoefficient, SwimThrust, and Mass in the Details panel for the desired feel.

Hook OnOxygenChanged and OnDrowned in Blueprint for HUD and VFX.

For nicer visuals, add:

camera bob/sway when swimming

particle bubbles when sprinting

post-process underwater tint when below surface

sound effects for swimming and drowning