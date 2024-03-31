import React from "react";
import { Gesture, GestureDetector } from "react-native-gesture-handler";
import { runOnJS } from "react-native-reanimated";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { Card, H4, Image, Stack, YStack } from "tamagui";

export const DemoCard = ({
  text,
  iconText,
  iconColor,
  size,
  children,
  setOpen,
  props,
}: any) => {
  const tap = Gesture.Tap().onStart(() => {
    if (setOpen) {
      runOnJS(setOpen)(true);
    }
  });
  return (
    <GestureDetector gesture={tap}>
      <Card
        size={"$4"}
        bordered
        backgroundColor={"white"}
        animation="bouncy"
        pressStyle={{ scale: 1.025 }}
        {...props}
      >
        <Card.Header flexDirection="column" gap={10} padded>
          {/* <MaterialCommunityIcons
            name={iconText}
            color={iconColor}
            size={size}
          /> */}
          <Image
            source={{
              uri: "https://picsum.photos/200/300",
              height: 130,
            }}
          />
          <YStack>
            {children}
            <H4 color={"black"} textAlign="left">
              {text}
            </H4>
          </YStack>
        </Card.Header>
        <Card.Background></Card.Background>
      </Card>
    </GestureDetector>
  );
};
