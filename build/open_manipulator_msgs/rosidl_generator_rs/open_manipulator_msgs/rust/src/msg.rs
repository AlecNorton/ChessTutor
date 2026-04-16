#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to open_manipulator_msgs__msg__JointPosition

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct JointPosition {

    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_name: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub position: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_accelerations_scaling_factor: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub max_velocity_scaling_factor: f64,

}



impl Default for JointPosition {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::JointPosition::default())
  }
}

impl rosidl_runtime_rs::Message for JointPosition {
  type RmwMsg = super::msg::rmw::JointPosition;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        position: msg.position.into(),
        max_accelerations_scaling_factor: msg.max_accelerations_scaling_factor,
        max_velocity_scaling_factor: msg.max_velocity_scaling_factor,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_name: msg.joint_name
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        position: msg.position.as_slice().into(),
      max_accelerations_scaling_factor: msg.max_accelerations_scaling_factor,
      max_velocity_scaling_factor: msg.max_velocity_scaling_factor,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_name: msg.joint_name
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      position: msg.position
          .into_iter()
          .collect(),
      max_accelerations_scaling_factor: msg.max_accelerations_scaling_factor,
      max_velocity_scaling_factor: msg.max_velocity_scaling_factor,
    }
  }
}


// Corresponds to open_manipulator_msgs__msg__KinematicsPose

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct KinematicsPose {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pose: geometry_msgs::msg::Pose,


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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::KinematicsPose::default())
  }
}

impl rosidl_runtime_rs::Message for KinematicsPose {
  type RmwMsg = super::msg::rmw::KinematicsPose;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Owned(msg.pose)).into_owned(),
        max_accelerations_scaling_factor: msg.max_accelerations_scaling_factor,
        max_velocity_scaling_factor: msg.max_velocity_scaling_factor,
        tolerance: msg.tolerance,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pose: geometry_msgs::msg::Pose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pose)).into_owned(),
      max_accelerations_scaling_factor: msg.max_accelerations_scaling_factor,
      max_velocity_scaling_factor: msg.max_velocity_scaling_factor,
      tolerance: msg.tolerance,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pose: geometry_msgs::msg::Pose::from_rmw_message(msg.pose),
      max_accelerations_scaling_factor: msg.max_accelerations_scaling_factor,
      max_velocity_scaling_factor: msg.max_velocity_scaling_factor,
      tolerance: msg.tolerance,
    }
  }
}


// Corresponds to open_manipulator_msgs__msg__OpenManipulatorState
/// CONSTANTS

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct OpenManipulatorState {
    /// Messages
    pub open_manipulator_moving_state: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub open_manipulator_actuator_state: std::string::String,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::OpenManipulatorState::default())
  }
}

impl rosidl_runtime_rs::Message for OpenManipulatorState {
  type RmwMsg = super::msg::rmw::OpenManipulatorState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        open_manipulator_moving_state: msg.open_manipulator_moving_state.as_str().into(),
        open_manipulator_actuator_state: msg.open_manipulator_actuator_state.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        open_manipulator_moving_state: msg.open_manipulator_moving_state.as_str().into(),
        open_manipulator_actuator_state: msg.open_manipulator_actuator_state.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      open_manipulator_moving_state: msg.open_manipulator_moving_state.to_string(),
      open_manipulator_actuator_state: msg.open_manipulator_actuator_state.to_string(),
    }
  }
}


