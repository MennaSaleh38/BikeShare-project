import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago':'chicago.csv','newyork': 'new_york_city.csv','washington':'washington.csv' } #Dict with KEY(city) and csv files as values
months=['january','february','march','april','may','june'] #A list of months found in csv files
days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday'] #a list of days found in csv files
filter=['month','day','both','none'] #a list of available filters that user can choose from

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

#asks user for the city they would like to shows its data
#validating there will be no typos/spaces that can cause errors
    while True:
            city=input("Which city would you like to check its data?Please choose from the below:\nchicago,newyork or washington : ")
            city=city.lower().replace(" ","")

#validating that city name is in the CITY_DATA dict to avoid any errors

            if city in CITY_DATA.keys():
                print("Great! You've chosen {}.. Let's proceed..\n".format(city.title()))
                break
            else: # in case if it wasn't in our dict. user will be asked to enter input again
                print("Seems like you've entered something wrong. Please try again")

#asking user if they would like to filter by month,day ,both or none at all

    while True:
            date_filter=input("Would you like to filter by day,month ,both or none at all? In case you don't want to apply any filters please type none: ").lower()
#validating that user entered a valid date filter

            if date_filter in filter:
                print("We will filter by {}\n ".format(date_filter))
                break
            else:
                print("Seems like you've entered someting wrong.Please try again\n")
# In case user chose to filter with any date
    if date_filter =='none':
        month=months
        day=days
#In case user chose to filter by month
    elif date_filter=='month':
        while True:
            month=input('Which month do you want to filter with?\n[January,February,March,April,May,June]: ').lower()
            day=days
#validating user enter valid month
            if month in months:
                print("Filtering data by month: {} ...".format(month.title()))
                break
            else:
                print("Seems like you've entered something wrong,please enter a valid month")
#in case user chose to filter by day
    elif date_filter=='day':
            while True:
                day=input("Which day do you want to filter with?\n[Monday,Tuesday,Wednesday,Thursday,Friday,Saturday or Sunday]: ").lower()
                month=months
#validating that user entered valid day
                if day in days:
                    print("Filtering data by day: {} ....".format(day.title()))
                    break
                else:
                    print("Seems like you've entered something wrong, please enter a valid day")
#In case user wants to filter by both (day/month)
    elif date_filter=='both' :
        while True:
            month=input("Which month do you want to filter with?\n[January,Febraury,March,April,May,June]:").lower()
            day=input("Which day do you want to filter with?\n[Monday,Tuesday,Wednesday,Thursday,Friday,Saturday or Sunday]: " ).lower()
#validating that user entered correct month and day
            if month in months and day in days:
                print("Filtering data by month:{} and by day:{} ....".format(month.title(),day.title()))
                break
            else:
                print("Seems like you've entered something wrong,please enter a valid month/day\n")

    print('-'*40)
    return city,month,day


def load_data(city,month,day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename=CITY_DATA.get(city)    #get value(filename) according to key(city) from predefined dict
    df=pd.read_csv(filename)        #loading dataframe using filename

    df['Start Time']= pd.to_datetime(df['Start Time'])  #converting start time column to datetime object
    df['Month']=df['Start Time'].dt.month_name()        #creating Month column from Start time
    df['Weekday']=df['Start Time'].dt.day_name()        #creating Weekday column from Start time

# Applying filters(if any) from previous function to dataframe to month and weekday columns
    if month != months:
        df=df[df['Month']==month.title()]
    if day != days:
        df=df[df['Weekday']==day.title()]
    print("Loading your data...")
    print('-'*40)

    return df


def time_stats(df):

    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame with filters applied

    """
    start_time = time.time()
    print('\nCalculating The Most Frequent Times of Travel...\n')

    popular_month=df['Month'].mode()[0]         #finding most common month
    popular_day=df['Weekday'].mode()[0]         #finding most common day
    df['Start hour']=df['Start Time'].dt.hour   #creating a new column to get start hour
    popular_hour=df['Start hour'].mode()[0]     #finding most common hour

#the following block of codes will be used to show
#more precise ouputs in case the user to decided to filter with month/day

    month_values=np.unique(df['Month'].values)   #returns ndarray with unique values from the month column in the dataframe
    day_values=np.unique(df['Weekday'].values)   #returns ndarray with unique values from the weekday column in the dataframe
#if the user chooses to filter by none:
#Our data has 6 months and 7 days
    if month_values.size==6 and day_values.size==7:
        print("The most common month is {}".format(popular_month))      #prints the most common month without filters
        print("The most common day is {}".format(popular_day))          #prints the most common day without filters
        print("The most common start hour is {}".format(popular_hour))  #prints the most common hour without filters

#if the user chooses to filter by month

    elif month_values.size==1 and day_values.size==7:
        print("The most common day is {}".format(popular_day))          #prints the most common day in filtered month
        print("The most common hour is {}".format(popular_hour))        #prints the most common day in filtered month

#if the user chooses to filter by day
    elif month_values.size==6 and day_values.size==1:
        print("The most common month is {}".format(popular_month))      #prints the most common month in filtered day
        print("The most common hour is {}".format(popular_hour))        #prints the most common hour in fultered day

#if the user chooses to filter by day and month
    elif month_values.size==1 and day_values.size==1:
        print("The most common hour is {}".format(popular_hour))     #prints the most common hour in filtered day and month

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return


def station_stats(df):

    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame with filters applied

    """

    start_time = time.time()
    print('\nCalculating The Most Popular Stations and Trip...\n')

#printing most common start station

    start_station=df['Start Station'].mode()[0]
    print('Most common start station is: {} .'.format(start_station))

#printing most common end station

    end_station=df['End Station'].mode()[0]
    print("Most common end station is: {} .".format(end_station))

#printing the most common start to end station
#by creating a new column called Start to end station
#and calculating count of travel from to start to end station

    df['Start Station to End Station']='from '+df['Start Station']+' to '+df['End Station']
    start_end_station=df['Start Station to End Station'].mode()[0]
    count_start_to_end=(df['Start Station to End Station']==start_end_station).value_counts()
    print('Most common trip from start to end station is:{} , count:{} '.format(start_end_station,count_start_to_end[True]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame with filters applied
    """
    start_time = time.time()
    print('\nCalculating Trip Duration...\n')

#prints total travel time
    total_travel_time=df['Trip Duration'].sum()
    print("Total travel time: {} seconds".format(total_travel_time))


# prints average travel time
    average_travel_time=df['Trip Duration'].mean()
    print("Average travel time: {} seconds".format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame with filters applied
    """
    start_time = time.time()
    print('\nCalculating User Stats...\n')

#prints count of each user types
#to_string() to show count only
    user_type=df['User Type'].value_counts().to_string()
    print('Count of each user type :\n{} '.format(user_type))

#following block of code to ensure no error runs in case user chooses Washington
#as there is no 'gender' and 'Birth year' data in washigtnon

    try:
#prints count of each gender
        gender_count=df['Gender'].value_counts().to_string()
        print('Count of each gender:\n{}'.format(gender_count))

#prints the earliest Year of Birth(yob)

        earliest_yob=int(df['Birth Year'].min())
        print('Earliest Birth Year: {}'.format(earliest_yob))

#prints the most recent Year of Birth(yob)

        most_recent_yob=int(df['Birth Year'].max())
        print('The most recent Birth Year: {}'.format(most_recent_yob))

#prints the most common Year of Birth(yob)

        most_common_yob=int(df['Birth Year'].mode()[0])
        print('The most common Birth Year: {}'.format(most_common_yob))

#if user chooses the city Washington
    except:
        print('Gender and birth year data is not available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(city):
    """
    Asks the user if they would like to print raw data
    it prints the first 5 rows of data
    and asks the user if they would like to check more from raw data
    printing 5 rows at a time, until user chooses no

    Args:
        (str) city- name of the city to get file

    """

    print('Raw data is available to display')

#get value(filename) according to key(city) from predefined dict

    raw_data_df=pd.read_csv(CITY_DATA.get(city))
    start_row=0    #index number for start row
    end_row=5      #index number for end row

    while True:
        display=input("Would you like to display 5 rows from raw data? Yes/No: ").lower()
        if display=='yes':

            print(raw_data_df[start_row:end_row])  #prints 5 rows of raw data
            start_row+=5                           #adds 5 to check next 5 rows
            end_row+=5                             #adds 5 to check next 5 rows
            print(display)
        else:
            break

    return


def main():

    while True:

        city,month,day=get_filters()
        df=load_data(city,month,day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city)
        restart=input("Would you like to restart the program?(Yes/No): ").lower()
        if restart !='yes':
            print('Thank you... Goodbye!')
            break


if __name__ == "__main__":
	main()
