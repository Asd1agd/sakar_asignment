// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from single_robo_custom_interface:msg/ClusterPoints.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "single_robo_custom_interface/msg/detail/cluster_points__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace single_robo_custom_interface
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ClusterPoints_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) single_robo_custom_interface::msg::ClusterPoints(_init);
}

void ClusterPoints_fini_function(void * message_memory)
{
  auto typed_message = static_cast<single_robo_custom_interface::msg::ClusterPoints *>(message_memory);
  typed_message->~ClusterPoints();
}

size_t size_function__ClusterPoints__points_arr(const void * untyped_member)
{
  (void)untyped_member;
  return 3;
}

const void * get_const_function__ClusterPoints__points_arr(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void * get_function__ClusterPoints__points_arr(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<double, 3> *>(untyped_member);
  return &member[index];
}

void fetch_function__ClusterPoints__points_arr(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const double *>(
    get_const_function__ClusterPoints__points_arr(untyped_member, index));
  auto & value = *reinterpret_cast<double *>(untyped_value);
  value = item;
}

void assign_function__ClusterPoints__points_arr(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<double *>(
    get_function__ClusterPoints__points_arr(untyped_member, index));
  const auto & value = *reinterpret_cast<const double *>(untyped_value);
  item = value;
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ClusterPoints_message_member_array[1] = {
  {
    "points_arr",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    3,  // array size
    false,  // is upper bound
    offsetof(single_robo_custom_interface::msg::ClusterPoints, points_arr),  // bytes offset in struct
    nullptr,  // default value
    size_function__ClusterPoints__points_arr,  // size() function pointer
    get_const_function__ClusterPoints__points_arr,  // get_const(index) function pointer
    get_function__ClusterPoints__points_arr,  // get(index) function pointer
    fetch_function__ClusterPoints__points_arr,  // fetch(index, &value) function pointer
    assign_function__ClusterPoints__points_arr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ClusterPoints_message_members = {
  "single_robo_custom_interface::msg",  // message namespace
  "ClusterPoints",  // message name
  1,  // number of fields
  sizeof(single_robo_custom_interface::msg::ClusterPoints),
  ClusterPoints_message_member_array,  // message members
  ClusterPoints_init_function,  // function to initialize message memory (memory has to be allocated)
  ClusterPoints_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ClusterPoints_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ClusterPoints_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace single_robo_custom_interface


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<single_robo_custom_interface::msg::ClusterPoints>()
{
  return &::single_robo_custom_interface::msg::rosidl_typesupport_introspection_cpp::ClusterPoints_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, single_robo_custom_interface, msg, ClusterPoints)() {
  return &::single_robo_custom_interface::msg::rosidl_typesupport_introspection_cpp::ClusterPoints_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
