import React from "react";
import { Gesture, GestureDetector } from "react-native-gesture-handler";
import { runOnJS } from "react-native-reanimated";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { Card, H4, H5, Image, Stack, YStack } from "tamagui";

export const DemoCard = ({
  text,
  location,
  rating,
  iconText,
  src,
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
              uri: src,
              height: 130,
            }}
            style={{
              borderRadius: 10,
              objectFit: "cover",
            }}
          />
          <YStack>
            {children}
            <H5
              color={"black"}
              fontWeight={"bold"}
              mb={-6}
              size={"$2"}
              textAlign="left"
            >
              {rating}/5
            </H5>
            <H4 color={"black"} textAlign="left">
              {text}
            </H4>
            <H5 color={"gray"} mt={-6} size={"$4"} textAlign="left">
              {location}
            </H5>
          </YStack>
        </Card.Header>
        <Card.Background></Card.Background>
      </Card>
    </GestureDetector>
  );
};
