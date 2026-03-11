// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from single_robo_custom_interface:msg/ClusterPoints.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__TRAITS_HPP_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "single_robo_custom_interface/msg/detail/cluster_points__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace single_robo_custom_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const ClusterPoints & msg,
  std::ostream & out)
{
  out << "{";
  // member: points_arr
  {
    if (msg.points_arr.size() == 0) {
      out << "points_arr: []";
    } else {
      out << "points_arr: [";
      size_t pending_items = msg.points_arr.size();
      for (auto item : msg.points_arr) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ClusterPoints & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: points_arr
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.points_arr.size() == 0) {
      out << "points_arr: []\n";
    } else {
      out << "points_arr:\n";
      for (auto item : msg.points_arr) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ClusterPoints & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace single_robo_custom_interface

namespace rosidl_generator_traits
{

[[deprecated("use single_robo_custom_interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const single_robo_custom_interface::msg::ClusterPoints & msg,
  std::ostream & out, size_t indentation = 0)
{
  single_robo_custom_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use single_robo_custom_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const single_robo_custom_interface::msg::ClusterPoints & msg)
{
  return single_robo_custom_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<single_robo_custom_interface::msg::ClusterPoints>()
{
  return "single_robo_custom_interface::msg::ClusterPoints";
}

template<>
inline const char * name<single_robo_custom_interface::msg::ClusterPoints>()
{
  return "single_robo_custom_interface/msg/ClusterPoints";
}

template<>
struct has_fixed_size<single_robo_custom_interface::msg::ClusterPoints>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<single_robo_custom_interface::msg::ClusterPoints>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<single_robo_custom_interface::msg::ClusterPoints>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__TRAITS_HPP_
