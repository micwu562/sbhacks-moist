import requests
import json

# GraphQL query extracted into a variable
def make_query(after):
  PAGE_SIZE = 40
  template = """
query TeacherSearchResultsPageQuery(
  $query: TeacherSearchQuery!
  $schoolID: ID
  $includeSchoolFilter: Boolean!
) {
  search: newSearch {
    ...TeacherSearchPagination_search_1ZLmLD
  }
  school: node(id: $schoolID) @include(if: $includeSchoolFilter) {
    __typename
    ... on School {
      name
    }
    id
  }
}

fragment TeacherSearchPagination_search_1ZLmLD on newSearch {
  teachers(query: $query, first: FIRST_PARAM, after: "AFTER_PARAM") {
    didFallback
    edges {
      cursor
      node {
        ...TeacherCard_teacher
        id
        __typename
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    resultCount
    filters {
      field
      options {
        value
        id
      }
    }
  }
}

fragment TeacherCard_teacher on Teacher {
  id
  legacyId
  avgRating
  numRatings
  ...CardFeedback_teacher
  ...CardSchool_teacher
  ...CardName_teacher
  ...TeacherBookmark_teacher
}

fragment CardFeedback_teacher on Teacher {
  wouldTakeAgainPercent
  avgDifficulty
}

fragment CardSchool_teacher on Teacher {
  department
  school {
    name
    id
  }
}

fragment CardName_teacher on Teacher {
  firstName
  lastName
}

fragment TeacherBookmark_teacher on Teacher {
  id
  isSaved
}
""".replace("FIRST_PARAM", str(PAGE_SIZE)).replace("AFTER_PARAM",after)
  return template

url = "https://www.ratemyprofessors.com/graphql"
headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": "Basic dGVzdDp0ZXN0",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
}

cursor = ""

for i in range(10000):
  data = {
      "query": make_query(cursor),
      "variables": {
          "query": {
              "text": "",
              "schoolID": "U2Nob29sLTEwNzc=",
              "fallback": True,
              "departmentID": "RGVwYXJ0bWVudC0xMQ=="
          },
          "schoolID": "U2Nob29sLTEwNzc=",
          "includeSchoolFilter": True
      }
  }
  response = requests.post(url, headers=headers, data=json.dumps(data))
  res_json = response.json()


  json_str = json.dumps(res_json, indent=4)
  # print(json_str)

  teachers = res_json["data"]["search"]["teachers"]["edges"]
  cursor = res_json["data"]["search"]["teachers"]["pageInfo"]["endCursor"]
  hasNextPage = res_json["data"]["search"]["teachers"]["pageInfo"]["hasNextPage"]

  with open("teachers.txt", "a") as f:


    # loop through teachers
    for teacher in teachers:
      # print name and legacyid, if teacher is computer science
      # if teacher["node"]["department"] != "Computer Science":
      #   continue
      f.write(teacher["node"]["firstName"] + " " + teacher["node"]["lastName"] + " " + str(teacher["node"]["legacyId"]) + "\n")

  # no teachers left
  if not hasNextPage:
    break


