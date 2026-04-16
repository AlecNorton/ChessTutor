#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__msg__JointPosition() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__msg__JointPosition__init(msg: *mut JointPosition) -> bool;
    fn open_manipulator_msgs__msg__JointPosition__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<JointPosition>, size: usize) -> bool;
    fn open_manipulator_msgs__msg__JointPosition__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<JointPosition>);
    fn open_manipulator_msgs__msg__JointPosition__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<JointPosition>, out_seq: *mut rosidl_runtime_rs::Sequence<JointPosition>) -> bool;
}

// Corresponds to open_manipulator_msgs__msg__JointPosition
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JointPosition {

    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_name: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_accelerations_scaling_factor: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_velocity_scaling_factor: f64,

}



impl Default for JointPosition {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__msg__JointPosition__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__msg__JointPosition__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for JointPosition {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__JointPosition__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__JointPosition__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__JointPosition__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for JointPosition {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for JointPosition where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/msg/JointPosition";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__msg__JointPosition() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__msg__KinematicsPose() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__msg__KinematicsPose__init(msg: *mut KinematicsPose) -> bool;
    fn open_manipulator_msgs__msg__KinematicsPose__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<KinematicsPose>, size: usize) -> bool;
    fn open_manipulator_msgs__msg__KinematicsPose__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<KinematicsPose>);
    fn open_manipulator_msgs__msg__KinematicsPose__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<KinematicsPose>, out_seq: *mut rosidl_runtime_rs::Sequence<KinematicsPose>) -> bool;
}

// Corresponds to open_manipulator_msgs__msg__KinematicsPose
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KinematicsPose {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::rmw::Pose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_accelerations_scaling_factor: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_velocity_scaling_factor: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tolerance: f64,

}



impl Default for KinematicsPose {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__msg__KinematicsPose__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__msg__KinematicsPose__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for KinematicsPose {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__KinematicsPose__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__KinematicsPose__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__KinematicsPose__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for KinematicsPose {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for KinematicsPose where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/msg/KinematicsPose";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__msg__KinematicsPose() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__msg__OpenManipulatorState() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__msg__OpenManipulatorState__init(msg: *mut OpenManipulatorState) -> bool;
    fn open_manipulator_msgs__msg__OpenManipulatorState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<OpenManipulatorState>, size: usize) -> bool;
    fn open_manipulator_msgs__msg__OpenManipulatorState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<OpenManipulatorState>);
    fn open_manipulator_msgs__msg__OpenManipulatorState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<OpenManipulatorState>, out_seq: *mut rosidl_runtime_rs::Sequence<OpenManipulatorState>) -> bool;
}

// Corresponds to open_manipulator_msgs__msg__OpenManipulatorState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// CONSTANTS

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct OpenManipulatorState {
    /// Messages
    pub open_manipulator_moving_state: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub open_manipulator_actuator_state: rosidl_runtime_rs::String,

}

impl OpenManipulatorState {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const IS_MOVING: &'static str = "IS_MOVING";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STOPPED: &'static str = "STOPPED";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ACTUATOR_ENABLED: &'static str = "ACTUATOR_ENABLED";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ACTUATOR_DISABLED: &'static str = "ACTUATOR_DISABLED";

}


impl Default for OpenManipulatorState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__msg__OpenManipulatorState__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__msg__OpenManipulatorState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for OpenManipulatorState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__OpenManipulatorState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__OpenManipulatorState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__msg__OpenManipulatorState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for OpenManipulatorState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for OpenManipulatorState where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/msg/OpenManipulatorState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__msg__OpenManipulatorState() }
  }
}


