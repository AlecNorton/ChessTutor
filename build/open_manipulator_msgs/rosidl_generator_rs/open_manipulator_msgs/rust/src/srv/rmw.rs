#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__GetJointPosition_Request() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__GetJointPosition_Request__init(msg: *mut GetJointPosition_Request) -> bool;
    fn open_manipulator_msgs__srv__GetJointPosition_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetJointPosition_Request>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__GetJointPosition_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetJointPosition_Request>);
    fn open_manipulator_msgs__srv__GetJointPosition_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetJointPosition_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetJointPosition_Request>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__GetJointPosition_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointPosition_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub planning_group: rosidl_runtime_rs::String,

}



impl Default for GetJointPosition_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__GetJointPosition_Request__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__GetJointPosition_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetJointPosition_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetJointPosition_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetJointPosition_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetJointPosition_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetJointPosition_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetJointPosition_Request where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/GetJointPosition_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__GetJointPosition_Request() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__GetJointPosition_Response() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__GetJointPosition_Response__init(msg: *mut GetJointPosition_Response) -> bool;
    fn open_manipulator_msgs__srv__GetJointPosition_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetJointPosition_Response>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__GetJointPosition_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetJointPosition_Response>);
    fn open_manipulator_msgs__srv__GetJointPosition_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetJointPosition_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetJointPosition_Response>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__GetJointPosition_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetJointPosition_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_position: super::super::msg::rmw::JointPosition,

}



impl Default for GetJointPosition_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__GetJointPosition_Response__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__GetJointPosition_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetJointPosition_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetJointPosition_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetJointPosition_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetJointPosition_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetJointPosition_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetJointPosition_Response where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/GetJointPosition_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__GetJointPosition_Response() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__GetKinematicsPose_Request() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__GetKinematicsPose_Request__init(msg: *mut GetKinematicsPose_Request) -> bool;
    fn open_manipulator_msgs__srv__GetKinematicsPose_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetKinematicsPose_Request>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__GetKinematicsPose_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetKinematicsPose_Request>);
    fn open_manipulator_msgs__srv__GetKinematicsPose_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetKinematicsPose_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetKinematicsPose_Request>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__GetKinematicsPose_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetKinematicsPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub planning_group: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub end_effector_name: rosidl_runtime_rs::String,

}



impl Default for GetKinematicsPose_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__GetKinematicsPose_Request__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__GetKinematicsPose_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetKinematicsPose_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetKinematicsPose_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetKinematicsPose_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetKinematicsPose_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetKinematicsPose_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetKinematicsPose_Request where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/GetKinematicsPose_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__GetKinematicsPose_Request() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__GetKinematicsPose_Response() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__GetKinematicsPose_Response__init(msg: *mut GetKinematicsPose_Response) -> bool;
    fn open_manipulator_msgs__srv__GetKinematicsPose_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetKinematicsPose_Response>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__GetKinematicsPose_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetKinematicsPose_Response>);
    fn open_manipulator_msgs__srv__GetKinematicsPose_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetKinematicsPose_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetKinematicsPose_Response>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__GetKinematicsPose_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetKinematicsPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub kinematics_pose: super::super::msg::rmw::KinematicsPose,

}



impl Default for GetKinematicsPose_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__GetKinematicsPose_Response__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__GetKinematicsPose_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetKinematicsPose_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetKinematicsPose_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetKinematicsPose_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__GetKinematicsPose_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetKinematicsPose_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetKinematicsPose_Response where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/GetKinematicsPose_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__GetKinematicsPose_Response() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetJointPosition_Request() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__SetJointPosition_Request__init(msg: *mut SetJointPosition_Request) -> bool;
    fn open_manipulator_msgs__srv__SetJointPosition_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetJointPosition_Request>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__SetJointPosition_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetJointPosition_Request>);
    fn open_manipulator_msgs__srv__SetJointPosition_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetJointPosition_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetJointPosition_Request>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__SetJointPosition_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointPosition_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub planning_group: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub joint_position: super::super::msg::rmw::JointPosition,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path_time: f64,

}



impl Default for SetJointPosition_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__SetJointPosition_Request__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__SetJointPosition_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetJointPosition_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetJointPosition_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetJointPosition_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetJointPosition_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetJointPosition_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetJointPosition_Request where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/SetJointPosition_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetJointPosition_Request() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetJointPosition_Response() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__SetJointPosition_Response__init(msg: *mut SetJointPosition_Response) -> bool;
    fn open_manipulator_msgs__srv__SetJointPosition_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetJointPosition_Response>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__SetJointPosition_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetJointPosition_Response>);
    fn open_manipulator_msgs__srv__SetJointPosition_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetJointPosition_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetJointPosition_Response>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__SetJointPosition_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetJointPosition_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_planned: bool,

}



impl Default for SetJointPosition_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__SetJointPosition_Response__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__SetJointPosition_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetJointPosition_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetJointPosition_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetJointPosition_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetJointPosition_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetJointPosition_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetJointPosition_Response where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/SetJointPosition_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetJointPosition_Response() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetKinematicsPose_Request() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__SetKinematicsPose_Request__init(msg: *mut SetKinematicsPose_Request) -> bool;
    fn open_manipulator_msgs__srv__SetKinematicsPose_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetKinematicsPose_Request>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__SetKinematicsPose_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetKinematicsPose_Request>);
    fn open_manipulator_msgs__srv__SetKinematicsPose_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetKinematicsPose_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetKinematicsPose_Request>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__SetKinematicsPose_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetKinematicsPose_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub planning_group: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub end_effector_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub kinematics_pose: super::super::msg::rmw::KinematicsPose,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path_time: f64,

}



impl Default for SetKinematicsPose_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__SetKinematicsPose_Request__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__SetKinematicsPose_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetKinematicsPose_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetKinematicsPose_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetKinematicsPose_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetKinematicsPose_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetKinematicsPose_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetKinematicsPose_Request where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/SetKinematicsPose_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetKinematicsPose_Request() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetKinematicsPose_Response() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__SetKinematicsPose_Response__init(msg: *mut SetKinematicsPose_Response) -> bool;
    fn open_manipulator_msgs__srv__SetKinematicsPose_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetKinematicsPose_Response>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__SetKinematicsPose_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetKinematicsPose_Response>);
    fn open_manipulator_msgs__srv__SetKinematicsPose_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetKinematicsPose_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetKinematicsPose_Response>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__SetKinematicsPose_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetKinematicsPose_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_planned: bool,

}



impl Default for SetKinematicsPose_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__SetKinematicsPose_Response__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__SetKinematicsPose_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetKinematicsPose_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetKinematicsPose_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetKinematicsPose_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetKinematicsPose_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetKinematicsPose_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetKinematicsPose_Response where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/SetKinematicsPose_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetKinematicsPose_Response() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetDrawingTrajectory_Request() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__SetDrawingTrajectory_Request__init(msg: *mut SetDrawingTrajectory_Request) -> bool;
    fn open_manipulator_msgs__srv__SetDrawingTrajectory_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetDrawingTrajectory_Request>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__SetDrawingTrajectory_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetDrawingTrajectory_Request>);
    fn open_manipulator_msgs__srv__SetDrawingTrajectory_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetDrawingTrajectory_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetDrawingTrajectory_Request>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__SetDrawingTrajectory_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetDrawingTrajectory_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub end_effector_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub drawing_trajectory_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub param: rosidl_runtime_rs::Sequence<f64>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub path_time: f64,

}



impl Default for SetDrawingTrajectory_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__SetDrawingTrajectory_Request__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__SetDrawingTrajectory_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetDrawingTrajectory_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetDrawingTrajectory_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetDrawingTrajectory_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetDrawingTrajectory_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetDrawingTrajectory_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetDrawingTrajectory_Request where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/SetDrawingTrajectory_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetDrawingTrajectory_Request() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetDrawingTrajectory_Response() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__SetDrawingTrajectory_Response__init(msg: *mut SetDrawingTrajectory_Response) -> bool;
    fn open_manipulator_msgs__srv__SetDrawingTrajectory_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetDrawingTrajectory_Response>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__SetDrawingTrajectory_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetDrawingTrajectory_Response>);
    fn open_manipulator_msgs__srv__SetDrawingTrajectory_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetDrawingTrajectory_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetDrawingTrajectory_Response>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__SetDrawingTrajectory_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetDrawingTrajectory_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_planned: bool,

}



impl Default for SetDrawingTrajectory_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__SetDrawingTrajectory_Response__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__SetDrawingTrajectory_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetDrawingTrajectory_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetDrawingTrajectory_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetDrawingTrajectory_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetDrawingTrajectory_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetDrawingTrajectory_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetDrawingTrajectory_Response where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/SetDrawingTrajectory_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetDrawingTrajectory_Response() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetActuatorState_Request() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__SetActuatorState_Request__init(msg: *mut SetActuatorState_Request) -> bool;
    fn open_manipulator_msgs__srv__SetActuatorState_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetActuatorState_Request>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__SetActuatorState_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetActuatorState_Request>);
    fn open_manipulator_msgs__srv__SetActuatorState_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetActuatorState_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SetActuatorState_Request>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__SetActuatorState_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetActuatorState_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub set_actuator_state: bool,

}



impl Default for SetActuatorState_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__SetActuatorState_Request__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__SetActuatorState_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetActuatorState_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetActuatorState_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetActuatorState_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetActuatorState_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetActuatorState_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetActuatorState_Request where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/SetActuatorState_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetActuatorState_Request() }
  }
}


#[link(name = "open_manipulator_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetActuatorState_Response() -> *const std::ffi::c_void;
}

#[link(name = "open_manipulator_msgs__rosidl_generator_c")]
extern "C" {
    fn open_manipulator_msgs__srv__SetActuatorState_Response__init(msg: *mut SetActuatorState_Response) -> bool;
    fn open_manipulator_msgs__srv__SetActuatorState_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SetActuatorState_Response>, size: usize) -> bool;
    fn open_manipulator_msgs__srv__SetActuatorState_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SetActuatorState_Response>);
    fn open_manipulator_msgs__srv__SetActuatorState_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SetActuatorState_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SetActuatorState_Response>) -> bool;
}

// Corresponds to open_manipulator_msgs__srv__SetActuatorState_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetActuatorState_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub is_planned: bool,

}



impl Default for SetActuatorState_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !open_manipulator_msgs__srv__SetActuatorState_Response__init(&mut msg as *mut _) {
        panic!("Call to open_manipulator_msgs__srv__SetActuatorState_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SetActuatorState_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetActuatorState_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetActuatorState_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { open_manipulator_msgs__srv__SetActuatorState_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SetActuatorState_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SetActuatorState_Response where Self: Sized {
  const TYPE_NAME: &'static str = "open_manipulator_msgs/srv/SetActuatorState_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__open_manipulator_msgs__srv__SetActuatorState_Response() }
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


