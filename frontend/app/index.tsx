import { ArrowRight } from "@tamagui/lucide-icons";
import { useRouter } from "expo-router";
import { Button, Image, Square, Text } from "tamagui";

import { MyStack } from "../components/MyStack";

import { ModerateScale, VerticalScale } from "./hooks/metrics";

export default function Home() {
  const router = useRouter();

  return (
    <MyStack
      justifyContent="center"
      alignItems="center"
      backgroundColor={"#FFFFFF"}
      padding={0}
    >
      <Image
        // marginTop={"15%"}
        height={"100%"}
        // alignSelf="center"
        // scale={0.9}
        // position="absolute"
        width={"100%"}
        resizeMode="contain"
        // height={"100%"}
        source={{
          uri: require("../assets/OPEN_HEALTH.png"),
          width: 400,
          height: 600,
        }}
      />
      <Square
        // margin={40}
        paddingLeft={"$4"}
        paddingRight={"$4"}
        width={"100%"}
        position="absolute"
        bottom={"2.5%"}
        justifyContent="flex-start"
        alignItems="flex-start"
        paddingTop={"$5"}
        paddingBottom={"$5"}
      >
        <Text
          fontSize={ModerateScale(22)}
          mb="$-2"
          fontWeight="bold"
          color={"black"}
        >
          Get started with your smile
        </Text>
        <Button
          width={"100%"}
          height={VerticalScale(55)}
          marginTop={12}
          borderColor={"black"}
          backgroundColor={"white"}
          fontWeight="bold"
          theme="red"
          iconAfter={<ArrowRight size={ModerateScale(16)} />}
          onPress={() => router.replace("/tabs")}
        >
          <Text fontWeight={"semibold"} fontSize={ModerateScale(14)}>
            Continue
          </Text>
        </Button>
      </Square>
    </MyStack>
  );
}
