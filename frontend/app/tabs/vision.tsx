import { useEffect, useRef, useState } from "react";
import {
  ArrowLeft,
  CircleDot,
  FlipHorizontal2,
  GalleryThumbnails,
  Send,
  X,
} from "@tamagui/lucide-icons";
import { Video } from "expo-av";
import { Camera, CameraType } from "expo-camera";
import * as FileSystem from "expo-file-system";
import * as MediaLibrary from "expo-media-library";
import { shareAsync } from "expo-sharing";
import {
  Adapt,
  Button,
  Dialog,
  Fieldset,
  H3,
  Image,
  Input,
  Label,
  Paragraph,
  ScrollView,
  Sheet,
  Text,
  TooltipSimple,
  Unspaced,
  View,
  XStack,
} from "tamagui";
import * as ImagePicker from "expo-image-picker";

import { MySafeAreaView } from "../../components/MySafeAreaView";
import { MyStack } from "../../components/MyStack";

export default function Vision() {
  const cameraRef: any = useRef();
  const [cameraDir, setCameraDir] = useState(CameraType.back);
  const [hasCameraPermission, setHasCameraPermission] = useState();
  const [hasMicrophonePermission, setHasMicrophonePermission] = useState();
  const [hasMediaLibraryPermission, setHasMediaLibraryPermission] = useState();
  const [isRecording, setIsRecording] = useState(false);
  const [video, setVideo] = useState<any>();
  const [picture, setPicture] = useState<any>();
  const [open, setOpen] = useState(false);
  const [image, setImage] = useState(null);
  const [text, setText] = useState("");
  const [modelTxt, setModelTxt] = useState("");

  useEffect(() => {
    if (image) {
      (async () => {
        const formData: any = new FormData();
        formData.append("image", {
          uri: image,
          name: "photo.jpg",
          type: "image/jpg",
        });

        try {
          const flaskResponse = await fetch("http://127.0.0.1:5000/pred", {
            method: "POST",
            body: formData,
          });

          if (!flaskResponse.ok) {
            throw new Error(
              `Request failed with status: ${flaskResponse.status}`
            );
          }

          const result = await flaskResponse.json();
          console.log(result);

          // Update state or perform other actions with the response
          setModelTxt(result); // Assuming result is a string or can be converted to one
        } catch (error) {
          console.error("Error:", error);
          // Handle errors as needed
        }
      })();
    } else if (picture) {
      (async () => {
        const formData: any = new FormData();
        formData.append("image", {
          uri: picture.uri,
          name: "photo.jpg",
          type: "image/jpg",
        });

        try {
          const flaskResponse = await fetch("http://127.0.0.1:5000/pred", {
            method: "POST",
            body: formData,
          });

          if (!flaskResponse.ok) {
            throw new Error(
              `Request failed with status: ${flaskResponse.status}`
            );
          }

          const result = await flaskResponse.json();
          console.log(result);

          // Update state or perform other actions with the response
          setModelTxt(result); // Assuming result is a string or can be converted to one
        } catch (error) {
          console.error("Error:", error);
          // Handle errors as needed
        }
      })();
    }
  }, [image, picture]);

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    console.log(result);

    if (!result.canceled) {
      setImage(result.assets[0].uri);
    }
  };

  useEffect(() => {
    (async () => {
      const cameraPermission: any =
        await Camera.requestCameraPermissionsAsync();
      const microphonePermission: any =
        await Camera.requestMicrophonePermissionsAsync();
      const mediaLibraryPermission: any =
        await MediaLibrary.requestPermissionsAsync();

      setHasCameraPermission(cameraPermission.status);
      setHasMicrophonePermission(microphonePermission.status);
      setHasMediaLibraryPermission(mediaLibraryPermission.status);
    })();
  }, []);

  if (
    hasCameraPermission === undefined ||
    hasMicrophonePermission === undefined
  ) {
    return <Text>Requestion permissions...</Text>;
  } else if (!hasCameraPermission) {
    return <Text>Permission for camera not granted.</Text>;
  }

  const recordVideo = () => {
    setIsRecording(true);
    const options = {
      quality: "1080p",
      maxDuration: 60,
      mute: false,
    };

    cameraRef.current.recordAsync(options).then((recordedVideo) => {
      setVideo(recordedVideo);
      setIsRecording(false);
    });
  };

  const reqModel = async () => {
    const response = await fetch("http://127.0.0.1:5000/llm", {
      method: "POST",
      body: JSON.stringify({ text_prompt: text }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const result = await response.json();
    console.log(result);
    setModelTxt(result);
  };

  const takePicture = async () => {
    const photo = await cameraRef.current.takePictureAsync();
    setPicture(photo.uri);

    console.log(photo);

    // const query = async (filename) => {
    //   try {
    //     const destinationUri = `${FileSystem.documentDirectory}${filename}`;
    //     const data = await FileSystem.readAsStringAsync(destinationUri, {
    //       encoding: FileSystem.EncodingType.Base64
    //     });

    //     const response = await fetch(
    //       "https://api-inference.huggingface.co/models/nateraw/food",
    //       {
    //         method: "POST",
    //         headers: {
    //           Authorization: "Bearer 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",
    //           "Content-Type": "application/json"
    //         },
    //         body: JSON.stringify({ data: data })
    //       }
    //     );

    //     if (!response.ok) {
    //       throw new Error(`Request failed with status: ${response.status}`);
    //     }

    //     const result = await response.json();
    //     return result;
    //   } catch (error) {
    //     console.error("Error:", error);
    //     throw error;
    //   }
    // // };

    // const filename = "myImage.jpg"; // Adjust the filename as needed

    // try {
    //   const destinationUri = `${FileSystem.documentDirectory}${filename}`;
    //   await FileSystem.copyAsync({ from: photo.uri, to: destinationUri });
    //   console.log("File copied successfully");

    //   // Call the query function to analyze the image
    //   const response = await query(filename);
    //   console.log(JSON.stringify(response));
    // } catch (error) {
    //   console.error("Error copying file:", error);
    // }

    MediaLibrary.saveToLibraryAsync(photo.uri).then(() => {
      setPicture(undefined);
    });
  };

  const stopRecording = () => {
    setIsRecording(false);
    cameraRef.current.stopRecording();
  };

  if (video) {
    const shareVideo = () => {
      shareAsync(video.uri).then(() => {
        setVideo(undefined);
      });
    };

    MediaLibrary.saveToLibraryAsync(video.uri).then(() => {
      setVideo(undefined);
    });

    return (
      <MySafeAreaView>
        <Video
          source={{ uri: video.uri }}
          useNativeControls
          // resizeMode="contain"
          isLooping
        />
        <Button onPress={shareVideo}>Share</Button>
        <Button onPress={() => setVideo(undefined)}>Discard</Button>
      </MySafeAreaView>
    );
  }

  return (
    <>
      {picture || image ? (
        <MySafeAreaView>
          <MyStack flexDirection="column" justifyContent="flex-start" gap={-5}>
            <XStack justifyContent="center" mb={"$6"} space="$5">
              <Button
                size={"$3"}
                style={{ position: "absolute", left: 0 }}
                icon={ArrowLeft}
                onPress={() => {
                  setPicture(undefined);
                  setImage(null);
                }}
              />
              {/* <H3>Smiler</H3> */}
            </XStack>

            <XStack alignItems="center" bottom={0} marginTop={"$5"} space="$2">
              <Input
                marginTop={"auto"}
                size={"$4"}
                flex={1}
                onChangeText={setText}
                placeholder="Enter your details..."
              />
              <Button onPress={() => reqModel()} size={"$4"}>
                <Send size={"$1"} />
              </Button>
            </XStack>

            <ScrollView padding={"$4"}>
              <Image
                source={{ uri: picture || image }}
                width={"100%"}
                height={300}
              />
              <Paragraph>{modelTxt && modelTxt}</Paragraph>
            </ScrollView>
          </MyStack>
        </MySafeAreaView>
      ) : (
        <Camera
          type={cameraDir}
          style={{
            width: "100%",
            height: "100%",
            justifyContent: "flex-end",
          }}
          ref={cameraRef}
        >
          <View
            flexDirection="row"
            alignItems="center"
            justifyContent="center"
            gap={9}
            marginBottom={32}
          >
            <Button onPress={pickImage}>
              <GalleryThumbnails />
            </Button>

            <Button
              size={85}
              w={80}
              borderRadius={"100px"}
              onPress={takePicture}
            >
              <CircleDot />
            </Button>
            <Button
              onPress={() =>
                cameraDir == CameraType.back
                  ? setCameraDir(CameraType.front)
                  : setCameraDir(CameraType.back)
              }
            >
              <FlipHorizontal2 />
            </Button>
          </View>
        </Camera>
      )}
    </>
  );
}
