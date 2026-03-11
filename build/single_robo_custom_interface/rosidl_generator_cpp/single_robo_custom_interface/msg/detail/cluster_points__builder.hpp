// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from single_robo_custom_interface:msg/ClusterPoints.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__BUILDER_HPP_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "single_robo_custom_interface/msg/detail/cluster_points__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace single_robo_custom_interface
{

namespace msg
{

namespace builder
{

class Init_ClusterPoints_points_arr
{
public:
  Init_ClusterPoints_points_arr()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::single_robo_custom_interface::msg::ClusterPoints points_arr(::single_robo_custom_interface::msg::ClusterPoints::_points_arr_type arg)
  {
    msg_.points_arr = std::move(arg);
    return std::move(msg_);
  }

private:
  ::single_robo_custom_interface::msg::ClusterPoints msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::single_robo_custom_interface::msg::ClusterPoints>()
{
  return single_robo_custom_interface::msg::builder::Init_ClusterPoints_points_arr();
}

}  // namespace single_robo_custom_interface

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__BUILDER_HPP_
