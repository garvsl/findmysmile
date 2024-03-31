import React, { createRef, useEffect, useRef, useState } from "react";
import { AnimatePresence, H4, ScrollView, Text, YStack } from "tamagui";
import { XStack } from "tamagui";

import { DemoCard } from "../../components/home/DemoCard";
import HeaderBar from "../../components/home/HeaderBar";
import SearchBar from "../../components/home/SearchBar";
import { SheetCard } from "../../components/home/SheetCard";
import { MySafeAreaView } from "../../components/MySafeAreaView";
import { MyStack } from "../../components/MyStack";

export default function Home() {
  const [defaultItems, setDefaultItems] = useState([
    {
      id: 123,
      text: "Center City Dental",
      iconText: "heart",
      iconColor: "red",
      size: 35,
      img: "https://s3-media0.fl.yelpcdn.com/bphoto/RRvjQm7HcAQSlK0FbkYtuQ/348s.jpg",
      rating: 4.2,
      location: "Philadelphia, PA",
    },
    {
      id: 223,
      text: "Lumia Dental",
      iconText: "pen",
      iconColor: "darkblue",
      size: 50,
      img: "https://s3-media0.fl.yelpcdn.com/bphoto/iVZT-6A_SG-eIFvTcP8nRg/348s.jpg",
      rating: 4.6,
      location: "New York, NY",
    },
    {
      id: 323,
      text: "Midtown Dental",
      iconText: "calendar",
      iconColor: "orange",
      size: 50,
      img: "https://s3-media0.fl.yelpcdn.com/bphoto/7OhCHksXs_F1QTTDGx5Pmw/348s.jpg",
      rating: 4.8,
      location: "New York, NY",
    },
    {
      id: 423,
      text: "Princeton Dental",
      iconText: "account-group",
      iconColor: "purple",
      size: 50,
      img: "https://s3-media0.fl.yelpcdn.com/bphoto/CecrwlP5ST91dksGj_JGHA/348s.jpg",
      rating: 4.9,
      location: "Princeton, NJ",
    },
    {
      id: 523,
      text: "Smile Craft",
      iconText: "plus-circle",
      iconColor: "green",
      size: 50,
      img: "https://s3-media0.fl.yelpcdn.com/bphoto/cndXaZREuTrJXRUy9YC-mw/348s.jpg",
      rating: 4.4,
      location: "Boston, MA",
    },
  ]);
  const [filteredItems, setFilteredItems] = useState(defaultItems);
  const [refs, setRefs] = useState([]);

  useEffect(() => {
    setRefs(defaultItems.map(() => createRef()));
    setFilteredItems(defaultItems);
  }, [defaultItems]);

  const handleDelete = (itemId) => {
    setDefaultItems((currentItems) =>
      currentItems.filter((item) => item.id !== itemId)
    );
  };
  const onSearch = (searchText) => {
    if (searchText) {
      const searchResults = defaultItems.filter((item) =>
        item.text.toLowerCase().includes(searchText.toLowerCase())
      );
      setFilteredItems(searchResults);
    } else {
      setFilteredItems(defaultItems);
    }
  };

  return (
    <MyStack
      flexDirection="column"
      justifyContent="flex-start"
      alignItems="center"
      padding={0}
      backgroundColor={"white"}
    >
      <MySafeAreaView width={"100%"} gap={25}>
        <YStack gap={30} padding={"3.5%"}>
          {/* <HeaderBar /> */}

          <XStack justifyContent="flex-start" flexDirection="column" gap={8}>
            <Text fontSize={"$7"} fontWeight={"600"} color={"black"}>
              Welcome Back!
            </Text>
            <SearchBar placeHolder={"Search clinics..."} onSearch={onSearch} />
          </XStack>
        </YStack>

        <ScrollView
          marginTop={-35}
          marginBottom={-35}
          scrollsToTop={true}
          onScroll={() => {
            refs.map(
              (e) => refs.length > 1 && e.current != null && e.current.close()
            );
          }}
          scrollEventThrottle={0}
          showsVerticalScrollIndicator={false}
          contentContainerStyle={{
            alignItems: "center",
            paddingBottom: 50,
            paddingTop: 20,
          }}
        >
          <YStack
            alignItems="center"
            gap={11}
            width={"100%"}
            paddingHorizontal={"$3"}
          >
            {filteredItems.length == 0 ? (
              <DemoCard
                text={"Theres nothing here..."}
                iconText={"magnify"}
                iconColor={"black"}
                size={25}
                props={{
                  width: "100%",
                }}
              />
            ) : (
              <AnimatePresence>
                {filteredItems.map((item, index) => {
                  return (
                    <SheetCard
                      ref={refs[index]}
                      key={index}
                      text={item.text}
                      src={item.img}
                      rating={item.rating}
                      location={item.location}
                      iconText={item.iconText}
                      iconColor={item.iconColor}
                      size={item.size}
                      func={() => {
                        refs.map(
                          (e) =>
                            refs.length > 1 &&
                            e.current != null &&
                            e != refs[index] &&
                            e.current.close()
                        );
                      }}
                      onDelete={() => handleDelete(item.id)}
                    />
                  );
                })}
              </AnimatePresence>
            )}
          </YStack>
        </ScrollView>
      </MySafeAreaView>
    </MyStack>
  );
}
