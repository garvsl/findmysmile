import { MaterialCommunityIcons } from "@expo/vector-icons";
import { Tabs } from "expo-router";
import { View } from "tamagui";

import {
  HorizontalScale,
  ModerateScale,
  VerticalScale,
} from "../hooks/metrics";
export default function Layout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarLabelStyle: {
          fontSize: 13,
        },
        tabBarIconStyle: {
          top: 4,
        },
        tabBarActiveTintColor: "tomato",
        tabBarLabelPosition: "below-icon",
        tabBarStyle: {
          alignItems: "center",
          backgroundColor: "#fff",
        },
      }}
    >
      <Tabs.Screen
        name="home"
        options={{
          title: "",
          tabBarIcon(props) {
            return <MaterialCommunityIcons name="home" {...props} size={35} />;
          },
        }}
      />
      {/* <Tabs.Screen
        name="calorie"
        options={{
          title: "Chat",
          tabBarIcon(props) {
            return (
              <MaterialCommunityIcons name="message" {...props} size={30} />
            );
          },
        }}
      /> */}
      <Tabs.Screen
        name="vision"
        options={{
          title: "",

          tabBarIcon(props: any) {
            return (
              <View
                justifyContent="center"
                alignItems="center"
                backgroundColor={`${props.focused ? "tomato" : "$red9"}`}
                height={VerticalScale(70)}
                width={HorizontalScale(70)}
                aspectRatio={1 / 1}
                borderRadius={100}
                top={-6}
              >
                <MaterialCommunityIcons
                  name="chat"
                  style={{ color: `${props.focused ? "white" : "white"}` }}
                  {...props}
                  size={ModerateScale(35)}
                />
              </View>
            );
          },
        }}
      />
      {/* <Tabs.Screen
        name="training"
        options={{
          title: "Training",
          tabBarIcon(props) {
            return (
              <MaterialCommunityIcons name="dumbbell" {...props} size={30} />
            );
          },
        }}
      /> */}

      <Tabs.Screen
        name="profile"
        options={{
          title: "",
          tabBarIcon(props) {
            return (
              <MaterialCommunityIcons name="face-man" {...props} size={35} />
            );
          },
        }}
      />
    </Tabs>
  );
}
