# Automatic Resume Builder
    Project Structure has been laid out as the following. For the sake of the reader, this brief introduction to the general architecture has been provided. 
| | |
|:--:|:--:|
| [Main Application](app.py) | [Application Config](lib/app_conf.py)|

## Data Architecture
    All data is persisted through REDIS. This includes user information, and any historic processed job postings. 

#### TODO
- [ ] Triple check all data persistence and access
  - [ ] Ensure information is being properly moved through this application.
  - [ ] Create an Admin Page to allow for basic information mangement
- 
