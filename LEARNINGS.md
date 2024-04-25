# Team1: PetPal

Terminal chat application for Assignment 1

## Team Name & Team Members:

**TeamName**: PetPal

**TeamMembers**: Chenguang Liu, Dao Zheng Chang, Zhequn Wu

## Goals

### Original Goals

Our idea is to build an application that can leverage technology to improve a pet owner’s experience. There are 2 main facets to our application. Firstly, we want to create a platform where pet owners can rate points of interest based on their experiences of bringing their pets there. Next, we want to create a service that helps pet owners to plan a day out with their pets.

### Achieved Goals

We have finished the first part, involving accepting coordinates from the user and returning them useful information about nearby points of interest (POI). This information includes reviews on the location, the score of the location and pets that have visited the POI. Additionally, a user can also create a profile to store favorite locations.

## Functionalities

The functionalities of our project are demonstrated through user interactions at various stages:

1. **Initial Setup**: Upon signing up, users are prompted to bind a pet from our comprehensive pet database, which includes details such as breed and name. We use a user_id and pet_id to establish a one-to-many relationship.
2. **Location-Based Services**: Users can query for nearby dog parks by posting to `/places`, where the database stores location information. Subsequent retrieval of all place information is done through a GET request to the same endpoint.
3. **Review System**: Users can search for reviews based on their current location. Each review includes details about the author, the pet, the place's rating, title, and content.
4. **Interactive Features**: Users can post their own reviews based on their location and add places to their list of favorites, which is managed through a many-to-many database relationship.
5. **Personalized Recommendations**: We aim to recommend the best places for users based on their pet’s breed and name.

## Challenges

This project has been a practical learning curve in translating specific requirements into database relationships and creating endpoints using the Flask framework. We encountered challenges in retrieving location-specific information, linking different schema relationships, and dockerizing our endpoints and database. To overcome these challenges, we sought guidance from various resources including ChatGPT, developer documentation, and Stack Overflow.

