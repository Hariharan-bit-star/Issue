Notes & advanced ideas

Units: This pawn uses a pragmatic mix of cm (Unreal units) and SI for forces. The forces and coefficients are tuned for good gameplay feel — you can convert to fully SI consistent if you want physical accuracy (multiply positions by 100, etc).

Waves / varying surface: Query a Water actor or a heightmap to compute local WaterLevelZ instead of a single flat plane.

Submersion fraction: Instead of origin-only submersion, compute hull/mesh bounds overlap with water to get a more realistic buoyant force.

Swimming animation: Drive animation blendspace by Velocity.Size() and bSprint, and trigger "breath" animation at surface.

Underwater physics component: Consider creating a UUnderwaterMovementComponent if you plan to reuse across pawns.

Example: use the uploaded map image (if helpful)

If you want to use the previously uploaded world-map image as a texture or level reference, here's its path (you can convert/serve it as needed):

sandbox:/mnt/data/A_Mercator_projection_of_a_world_map_in_the_digita.png

If you want, I can next:

convert this into a MovementComponent (clean separation),

add wave-height sampling to compute local WaterLevelZ,

provide a Blueprint-ready version with camera shakes & VFX,

or tune parameters for a realistic scuba diver vs arcade swimmer feel.

  UCLASS()
  class YOUR_PROJECT_API AFlyingPawn : public APawn
  {
      GENERATED_BODY()

  public:
      AFlyingPawn();

  protected:
      virtual void BeginPlay() override;

  public:
      virtual void Tick(float DeltaTime) override;
      virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

      // Components
      UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
      class UStaticMeshComponent* PlaneMesh;

      UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
      class USpringArmComponent* SpringArm;

      UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
      class UCameraComponent* Camera;

      // Flight Parameters
      UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flight")
      float MaxSpeed = 2000.0f;

      UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flight")
      float Acceleration = 1000.0f;

      UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flight")
      float PitchSpeed = 50.0f;

      UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flight")
      float YawSpeed = 50.0f;

      UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flight")
      float RollSpeed = 100.0f;

      UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flight")
      float Drag = 0.1f;

      UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flight")
      float LiftForce = 500.0f;

      UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Flight")
      float BankingInfluence = 0.3f;

  private:
      // Input handlers
      void ThrottleInput(float Value);
      void PitchInput(float Value);
      void YawInput(float Value);
      void RollInput(float Value);
      void BrakeInput();
      void ReleaseBrake();

      // Flight state
      FVector Velocity;
      float CurrentThrottle = 0.0f;
      float CurrentPitch = 0.0f;
      float CurrentYaw = 0.0f;
      float CurrentRoll = 0.0f;
      bool bIsBraking = false;

      // Helper functions
      void UpdateMovement(float DeltaTime);
      void ApplyRotation(float DeltaTime);
      void ApplyPhysics(float DeltaTime);
  };

  FlyingPawn.cpp:

  #include "FlyingPawn.h"
  #include "Components/StaticMeshComponent.h"
  #include "Camera/CameraComponent.h"
  #include "GameFramework/SpringArmComponent.h"
  #include "Components/InputComponent.h"
  #include "Engine/Engine.h"

  AFlyingPawn::AFlyingPawn()
  {
      PrimaryActorTick.bCanEverTick = true;

      // Create root mesh component
      PlaneMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("PlaneMesh"));
      RootComponent = PlaneMesh;
      PlaneMesh->SetSimulatePhysics(false);
      PlaneMesh->SetEnableGravity(false);

      // Create spring arm
      SpringArm = CreateDefaultSubobject<USpringArmComponent>(TEXT("SpringArm"));
      SpringArm->SetupAttachment(RootComponent);
      SpringArm->TargetArmLength = 500.0f;
      SpringArm->bDoCollisionTest = false;

      // Create camera
      Camera = CreateDefaultSubobject<UCameraComponent>(TEXT("Camera"));
      Camera->SetupAttachment(SpringArm, USpringArmComponent::SocketName);

      Velocity = FVector::ZeroVector;
  }

  void AFlyingPawn::BeginPlay()
  {
      Super::BeginPlay();
  }

  void AFlyingPawn::Tick(float DeltaTime)
  {
      Super::Tick(DeltaTime);

      UpdateMovement(DeltaTime);
      ApplyRotation(DeltaTime);
      ApplyPhysics(DeltaTime);
  }

  void AFlyingPawn::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
  {
      Super::SetupPlayerInputComponent(PlayerInputComponent);

      // Bind axis inputs
      PlayerInputComponent->BindAxis("Throttle", this, &AFlyingPawn::ThrottleInput);
      PlayerInputComponent->BindAxis("Pitch", this, &AFlyingPawn::PitchInput);
      PlayerInputComponent->BindAxis("Yaw", this, &AFlyingPawn::YawInput);
      PlayerInputComponent->BindAxis("Roll", this, &AFlyingPawn::RollInput);

      // Bind action inputs
      PlayerInputComponent->BindAction("Brake", IE_Pressed, this, &AFlyingPawn::BrakeInput);
      PlayerInputComponent->BindAction("Brake", IE_Released, this, &AFlyingPawn::ReleaseBrake);
  }

  void AFlyingPawn::ThrottleInput(float Value)
  {
      CurrentThrottle = FMath::Clamp(Value, -1.0f, 1.0f);
  }

  void AFlyingPawn::PitchInput(float Value)
  {
      CurrentPitch = Value;
  }

  void AFlyingPawn::YawInput(float Value)
  {
      CurrentYaw = Value;
  }

  void AFlyingPawn::RollInput(float Value)
  {
      CurrentRoll = Value;
  }

  void AFlyingPawn::BrakeInput()
  {
      bIsBraking = true;
  }

  void AFlyingPawn::ReleaseBrake()
  {
      bIsBraking = false;
  }

  void AFlyingPawn::UpdateMovement(float DeltaTime)
  {
      if (bIsBraking)
      {
          // Apply braking force
          Velocity *= FMath::Max(0.0f, 1.0f - (5.0f * DeltaTime));
      }
      else
      {
          // Apply throttle acceleration
          FVector ForwardForce = GetActorForwardVector() * CurrentThrottle * Acceleration * DeltaTime;
          Velocity += ForwardForce;
      }

      // Apply drag
      Velocity *= (1.0f - Drag * DeltaTime);

      // Clamp to max speed
      float CurrentSpeed = Velocity.Size();
      if (CurrentSpeed > MaxSpeed)
      {
          Velocity = Velocity.GetSafeNormal() * MaxSpeed;
      }

      // Move the pawn
      FVector NewLocation = GetActorLocation() + (Velocity * DeltaTime);
      SetActorLocation(NewLocation, true);
  }

  void AFlyingPawn::ApplyRotation(float DeltaTime)
  {
      FRotator DeltaRotation = FRotator::ZeroRotator;

      // Apply pitch (up/down)
      DeltaRotation.Pitch = CurrentPitch * PitchSpeed * DeltaTime;

      // Apply yaw (left/right turning)
      DeltaRotation.Yaw = CurrentYaw * YawSpeed * DeltaTime;

      // Apply roll (banking)
      DeltaRotation.Roll = CurrentRoll * RollSpeed * DeltaTime;

      // Add banking influence when turning
      if (FMath::Abs(CurrentYaw) > 0.01f)
      {
          DeltaRotation.Roll += CurrentYaw * RollSpeed * BankingInfluence * DeltaTime;
      }

      AddActorLocalRotation(DeltaRotation);
  }

  void AFlyingPawn::ApplyPhysics(float DeltaTime)
  {
      // Apply lift based on forward velocity
      float Speed = Velocity.Size();
      float LiftAmount = (Speed / MaxSpeed) * LiftForce;

      FVector LiftVector = GetActorUpVector() * LiftAmount * DeltaTime;
      Velocity += LiftVector;

      // Apply gravity effect
      Velocity += FVector(0, 0, -980.0f) * DeltaTime * 0.2f; // Reduced gravity for flight

      