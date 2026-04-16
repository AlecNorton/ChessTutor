#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to open_manipulator_msgs__srv__GetJointPosition_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointPosition_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub planning_group: std::string::String,

}



impl Default for GetJointPosition_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetJointPosition_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetJointPosition_Request {
  type RmwMsg = super::srv::rmw::GetJointPosition_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        planning_group: msg.planning_group.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        planning_group: msg.planning_group.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      planning_group: msg.planning_group.to_string(),
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__GetJointPosition_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointPosition_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_position: super::msg::JointPosition,

}



impl Default for GetJointPosition_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetJointPosition_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetJointPosition_Response {
  type RmwMsg = super::srv::rmw::GetJointPosition_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_position: super::msg::JointPosition::into_rmw_message(std::borrow::Cow::Owned(msg.joint_position)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_position: super::msg::JointPosition::into_rmw_message(std::borrow::Cow::Borrowed(&msg.joint_position)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_position: super::msg::JointPosition::from_rmw_message(msg.joint_position),
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__GetKinematicsPose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetKinematicsPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub planning_group: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub end_effector_name: std::string::String,

}



impl Default for GetKinematicsPose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetKinematicsPose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetKinematicsPose_Request {
  type RmwMsg = super::srv::rmw::GetKinematicsPose_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        planning_group: msg.planning_group.as_str().into(),
        end_effector_name: msg.end_effector_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        planning_group: msg.planning_group.as_str().into(),
        end_effector_name: msg.end_effector_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      planning_group: msg.planning_group.to_string(),
      end_effector_name: msg.end_effector_name.to_string(),
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__GetKinematicsPose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetKinematicsPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub kinematics_pose: super::msg::KinematicsPose,

}



impl Default for GetKinematicsPose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetKinematicsPose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetKinematicsPose_Response {
  type RmwMsg = super::srv::rmw::GetKinematicsPose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        kinematics_pose: super::msg::KinematicsPose::into_rmw_message(std::borrow::Cow::Owned(msg.kinematics_pose)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        kinematics_pose: super::msg::KinematicsPose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.kinematics_pose)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      kinematics_pose: super::msg::KinematicsPose::from_rmw_message(msg.kinematics_pose),
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__SetJointPosition_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointPosition_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub planning_group: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_position: super::msg::JointPosition,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path_time: f64,

}



impl Default for SetJointPosition_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetJointPosition_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetJointPosition_Request {
  type RmwMsg = super::srv::rmw::SetJointPosition_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        planning_group: msg.planning_group.as_str().into(),
        joint_position: super::msg::JointPosition::into_rmw_message(std::borrow::Cow::Owned(msg.joint_position)).into_owned(),
        path_time: msg.path_time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        planning_group: msg.planning_group.as_str().into(),
        joint_position: super::msg::JointPosition::into_rmw_message(std::borrow::Cow::Borrowed(&msg.joint_position)).into_owned(),
      path_time: msg.path_time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      planning_group: msg.planning_group.to_string(),
      joint_position: super::msg::JointPosition::from_rmw_message(msg.joint_position),
      path_time: msg.path_time,
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__SetJointPosition_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointPosition_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_planned: bool,

}



impl Default for SetJointPosition_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetJointPosition_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetJointPosition_Response {
  type RmwMsg = super::srv::rmw::SetJointPosition_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        is_planned: msg.is_planned,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      is_planned: msg.is_planned,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      is_planned: msg.is_planned,
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__SetKinematicsPose_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetKinematicsPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub planning_group: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub end_effector_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub kinematics_pose: super::msg::KinematicsPose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path_time: f64,

}



impl Default for SetKinematicsPose_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetKinematicsPose_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetKinematicsPose_Request {
  type RmwMsg = super::srv::rmw::SetKinematicsPose_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        planning_group: msg.planning_group.as_str().into(),
        end_effector_name: msg.end_effector_name.as_str().into(),
        kinematics_pose: super::msg::KinematicsPose::into_rmw_message(std::borrow::Cow::Owned(msg.kinematics_pose)).into_owned(),
        path_time: msg.path_time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        planning_group: msg.planning_group.as_str().into(),
        end_effector_name: msg.end_effector_name.as_str().into(),
        kinematics_pose: super::msg::KinematicsPose::into_rmw_message(std::borrow::Cow::Borrowed(&msg.kinematics_pose)).into_owned(),
      path_time: msg.path_time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      planning_group: msg.planning_group.to_string(),
      end_effector_name: msg.end_effector_name.to_string(),
      kinematics_pose: super::msg::KinematicsPose::from_rmw_message(msg.kinematics_pose),
      path_time: msg.path_time,
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__SetKinematicsPose_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetKinematicsPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_planned: bool,

}



impl Default for SetKinematicsPose_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetKinematicsPose_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetKinematicsPose_Response {
  type RmwMsg = super::srv::rmw::SetKinematicsPose_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        is_planned: msg.is_planned,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      is_planned: msg.is_planned,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      is_planned: msg.is_planned,
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__SetDrawingTrajectory_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetDrawingTrajectory_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub end_effector_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drawing_trajectory_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub param: Vec<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path_time: f64,

}



impl Default for SetDrawingTrajectory_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetDrawingTrajectory_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetDrawingTrajectory_Request {
  type RmwMsg = super::srv::rmw::SetDrawingTrajectory_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        end_effector_name: msg.end_effector_name.as_str().into(),
        drawing_trajectory_name: msg.drawing_trajectory_name.as_str().into(),
        param: msg.param.into(),
        path_time: msg.path_time,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        end_effector_name: msg.end_effector_name.as_str().into(),
        drawing_trajectory_name: msg.drawing_trajectory_name.as_str().into(),
        param: msg.param.as_slice().into(),
      path_time: msg.path_time,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      end_effector_name: msg.end_effector_name.to_string(),
      drawing_trajectory_name: msg.drawing_trajectory_name.to_string(),
      param: msg.param
          .into_iter()
          .collect(),
      path_time: msg.path_time,
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__SetDrawingTrajectory_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetDrawingTrajectory_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_planned: bool,

}



impl Default for SetDrawingTrajectory_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetDrawingTrajectory_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetDrawingTrajectory_Response {
  type RmwMsg = super::srv::rmw::SetDrawingTrajectory_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        is_planned: msg.is_planned,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      is_planned: msg.is_planned,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      is_planned: msg.is_planned,
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__SetActuatorState_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetActuatorState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub set_actuator_state: bool,

}



impl Default for SetActuatorState_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetActuatorState_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetActuatorState_Request {
  type RmwMsg = super::srv::rmw::SetActuatorState_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        set_actuator_state: msg.set_actuator_state,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      set_actuator_state: msg.set_actuator_state,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      set_actuator_state: msg.set_actuator_state,
    }
  }
}


// Corresponds to open_manipulator_msgs__srv__SetActuatorState_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetActuatorState_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_planned: bool,

}



impl Default for SetActuatorState_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetActuatorState_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetActuatorState_Response {
  type RmwMsg = super::srv::rmw::SetActuatorState_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        is_planned: msg.is_planned,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      is_planned: msg.is_planned,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      is_planned: msg.is_planned,
    }
  }
}






#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__GetJointPosition() -> *const std::ffi::c_void;
}

// Corresponds to open_manipulator_msgs__srv__GetJointPosition
#[allow(missing_docs, non_camel_case_types)]
pub struct GetJointPosition;

impl rosidl_runtime_rs::Service for GetJointPosition {
    type Request = GetJointPosition_Request;
    type Response = GetJointPosition_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__GetJointPosition() }
    }
}




#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__GetKinematicsPose() -> *const std::ffi::c_void;
}

// Corresponds to open_manipulator_msgs__srv__GetKinematicsPose
#[allow(missing_docs, non_camel_case_types)]
pub struct GetKinematicsPose;

impl rosidl_runtime_rs::Service for GetKinematicsPose {
    type Request = GetKinematicsPose_Request;
    type Response = GetKinematicsPose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__GetKinematicsPose() }
    }
}




#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__SetJointPosition() -> *const std::ffi::c_void;
}

// Corresponds to open_manipulator_msgs__srv__SetJointPosition
#[allow(missing_docs, non_camel_case_types)]
pub struct SetJointPosition;

impl rosidl_runtime_rs::Service for SetJointPosition {
    type Request = SetJointPosition_Request;
    type Response = SetJointPosition_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__SetJointPosition() }
    }
}




#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__SetKinematicsPose() -> *const std::ffi::c_void;
}

// Corresponds to open_manipulator_msgs__srv__SetKinematicsPose
#[allow(missing_docs, non_camel_case_types)]
pub struct SetKinematicsPose;

impl rosidl_runtime_rs::Service for SetKinematicsPose {
    type Request = SetKinematicsPose_Request;
    type Response = SetKinematicsPose_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__SetKinematicsPose() }
    }
}




#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__SetDrawingTrajectory() -> *const std::ffi::c_void;
}

// Corresponds to open_manipulator_msgs__srv__SetDrawingTrajectory
#[allow(missing_docs, non_camel_case_types)]
pub struct SetDrawingTrajectory;

impl rosidl_runtime_rs::Service for SetDrawingTrajectory {
    type Request = SetDrawingTrajectory_Request;
    type Response = SetDrawingTrajectory_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__SetDrawingTrajectory() }
    }
}




#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__SetActuatorState() -> *const std::ffi::c_void;
}

// Corresponds to open_manipulator_msgs__srv__SetActuatorState
#[allow(missing_docs, non_camel_case_types)]
pub struct SetActuatorState;

impl rosidl_runtime_rs::Service for SetActuatorState {
    type Request = SetActuatorState_Request;
    type Response = SetActuatorState_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__open_manipulator_msgs__srv__SetActuatorState() }
    }
}


