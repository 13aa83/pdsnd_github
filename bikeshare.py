import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("Enter the name of the city (Chicago, New York City, or Washington): ").lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print("Invalid input. Please enter a valid city name.")


    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while month not in ['january', 'february', 'march', 'april', 'may','june','all']:
        month = input("Enter the name of the month: ").lower()
        if month not in ['january', 'february', 'march', 'april', 'may','june','all']:
            print("Invalid input. Please enter a valid month.")


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday','all']:
        day = input("Enter the name of the day: ").lower()
        if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday','saturday','sunday','all']:
            print("Invalid input. Please enter a valid day.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime('%A').str.lower()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.lower()]
    
    return df

def iterate_raw(city,month,day):
    counter = 0
    df = load_data(city, month, day)
    # Loop until the user says they don't want to see more data or there's no more data left to display
    while True:
        # Prompt the user if they want to see the next 5 lines of data
        show_data = input("Do you want to see the next 5 lines of raw data? Enter 'yes' or 'no': ")
        
        # If the user says 'no', exit the loop
        if show_data.lower() == 'no':
            break
        
        # If the user says 'yes', display the next 5 lines of data and update the counter
        elif show_data.lower() == 'yes':
            print(df[counter:counter+5])
            counter += 5
        
        # If the user enters something other than 'yes' or 'no', ask again
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("The most common month is ",df['Start Time'].dt.month.mode()[0])

    # TO DO: display the most common day of week
    print("The most common day of week is ",df['Start Time'].dt.dayofweek.mode()[0])


    # TO DO: display the most common start hour
    print("The most common start hour is ", df['Start Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most commonly used start station is ", df['End Station'].mode()[0])


    # TO DO: display most frequent combination of start station and end station trip
    df['start_end'] = df['Start Station'] + ' ' + df['End Station']
    print("The most frequent combination of start station and end station trip is ",df['start_end'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total travel time is ", sum(df['Trip Duration']))

    # TO DO: display mean travel time
    print("The average trip travel time is ", np.mean(df['Trip Duration']))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
        print(df['Gender'].value_counts())
    except:
        print("No Gender column available")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print("Earliest, most recent, and most common year of birth are respectively, ", min(df['Birth Year']), max(df['Birth Year']), df['Birth Year'].mode()[0])
    except:
        print("No Birth Year column available")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        iterate_raw(city, month, day)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
