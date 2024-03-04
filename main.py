import pandas as pd
import matplotlib.pyplot as plt

def clean_data(csv_df):
    # Clean data
    csv_df['Ciclo_Estacion_Retiro'] = csv_df['Ciclo_Estacion_Retiro'].apply(lambda x: x.split('-')[0])
    csv_df['Ciclo_EstacionArribo'] = csv_df['Ciclo_EstacionArribo'].apply(lambda x: x.split('-')[0])

    # Convert date and time columns to datetime type
    csv_df['Fecha_Retiro'] = pd.to_datetime(csv_df['Fecha_Retiro'], format='%d/%m/%Y')
    csv_df['Hora_Retiro'] = pd.to_datetime(csv_df['Hora_Retiro'], format='%H:%M:%S')
    csv_df['Fecha Arribo'] = pd.to_datetime(csv_df['Fecha Arribo'], format='%d/%m/%Y')
    csv_df['Hora_Arribo'] = pd.to_datetime(csv_df['Hora_Arribo'], format='%H:%M:%S')

    return csv_df

def more_used_stations(csv_df, month_year):
    # Combine the departure and arrival columns to get all used stations
    used_stations_csv = pd.concat([csv_df['Ciclo_Estacion_Retiro'], csv_df['Ciclo_EstacionArribo']])

    # Get the most used station
    most_used_station_csv = used_stations_csv.mode()[0]

    # Filter the DataFrame for the most used station and make a copy
    station_df = csv_df[(csv_df['Ciclo_Estacion_Retiro'] == most_used_station_csv) | (
                csv_df['Ciclo_EstacionArribo'] == most_used_station_csv)].copy()

    # Convert date and time columns to datetime type
    station_df['Hora_Retiro'] = pd.to_datetime(station_df['Hora_Retiro'], format='%H:%M:%S')
    station_df['Hora_Arribo'] = pd.to_datetime(station_df['Hora_Arribo'], format='%H:%M:%S')

    # Get the usage hours of the most used station
    usage_hours = pd.concat([station_df['Hora_Retiro'].dt.hour, station_df['Hora_Arribo'].dt.hour])

    # Plot the usage hours
    usage_hours.value_counts().sort_index().plot(kind='bar', figsize=(10, 6))
    plt.title('Horas de uso de la estación más utilizada ' + month_year)
    plt.xlabel('Hora del día')
    plt.ylabel('Numero de usos')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(month_year + '_more_used_stations.png')
    plt.show()

def bike_wear_per_year(csv_df, month_year):

    # Calculate the number of times each bike has been used
    bike_wear = pd.concat([csv_df['Bici']])

    # Get the most used bikes
    most_used_bikes = bike_wear.value_counts().head(10)

    print("Bikes with the most wear and tear per year are in " + month_year)
    print(most_used_bikes)

def explore_relationships_between_gender_and_age_of_users(csv_df, month_year):
    # Filtrar los datos por género
    male_data = csv_df[csv_df['Genero_Usuario'] == 'M']
    female_data = csv_df[csv_df['Genero_Usuario'] == 'F']
    other_data = csv_df[csv_df['Genero_Usuario'] == 'O']

    # Crear histogramas por género y edad
    plt.figure(figsize=(10, 6))
    plt.hist(male_data['Edad_Usuario'], bins=20, color='blue', alpha=0.5, label='Male')
    plt.hist(female_data['Edad_Usuario'], bins=20, color='pink', alpha=0.5, label='Female')
    plt.hist(other_data['Edad_Usuario'], bins=20, color='green', alpha=0.5, label='Other')

    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.title('Distribution of Age by Gender ' + month_year)
    plt.legend()
    plt.savefig(month_year + '_explore_relationships_between_gender_and_age_of_users.png')
    plt.show()

def most_congested_arrival_stations(csv_df, month_year):
    # Clean data
    csv_df['Ciclo_Estacion_Retiro'] = csv_df['Ciclo_Estacion_Retiro'].apply(lambda x: x.split('-')[0])
    csv_df['Ciclo_EstacionArribo'] = csv_df['Ciclo_EstacionArribo'].apply(lambda x: x.split('-')[0])

    # Convert date and time columns to datetime type
    csv_df['Fecha_Retiro'] = pd.to_datetime(csv_df['Fecha_Retiro'], format='%d/%m/%Y')
    csv_df['Hora_Retiro'] = pd.to_datetime(csv_df['Hora_Retiro'], format='%H:%M:%S')
    csv_df['Fecha Arribo'] = pd.to_datetime(csv_df['Fecha Arribo'], format='%d/%m/%Y')
    csv_df['Hora_Arribo'] = pd.to_datetime(csv_df['Hora_Arribo'], format='%H:%M:%S')

    top_arrival = csv_df['Ciclo_EstacionArribo'].value_counts().head(10)
    plt.figure(figsize=(10, 8))
    top_arrival.plot(kind='bar', title='Top 5 Estaciones de Arribo Más Saturadas ' + month_year)
    plt.xlabel('Estación de Arribo')
    plt.ylabel('Número de llegadas')
    plt.savefig(month_year + '_most_congested_arrival_stations.png')
    plt.show()

def most_congested_withdrawal_stations(csv_df, month_year):
    csv_df = clean_data(csv_df)

    top_withdrawal = csv_df['Ciclo_Estacion_Retiro'].value_counts().head(10)
    plt.figure(figsize=(10, 8))
    top_withdrawal.plot(kind='bar', title='Top 5 Estaciones de Retiro Más Saturadas ' + month_year)
    plt.xlabel('Estación de Retiro')
    plt.ylabel('Número de retiros')
    plt.savefig(month_year + '_most_congested_withdrawal_stations.png')
    plt.show()


def most_frequented_routes(csv_df, month_year):
    csv_df = clean_data(csv_df)
    most_frequented_routes = csv_df.groupby(['Ciclo_Estacion_Retiro', 'Ciclo_EstacionArribo']).size().nlargest(5)
    plt.figure(figsize=(10, 10))
    most_frequented_routes.plot(kind='bar', title='Top 5 Trayectos Más Recorridos ' + month_year)
    plt.xlabel('Trayecto')
    plt.ylabel('Número de viajes')
    plt.savefig(month_year + '_most_frequented_routes.png')
    plt.show()

def traffic_at_the_most_used_stations(csv_df, month_year):
    csv_df = clean_data(csv_df)
    top_used_stations = pd.concat(
        [csv_df['Ciclo_Estacion_Retiro'], csv_df['Ciclo_EstacionArribo']]).value_counts().head(10)
    plt.figure(figsize=(10, 8))
    top_used_stations.plot(kind='bar', title='Top 5 Estaciones Más Usadas ' + month_year)
    plt.xlabel('Estación')
    plt.ylabel('Número de usos')
    plt.savefig(month_year + '_traffic_at_the_most_used_stations.png')
    plt.show()

def traffic_at_the_most_congested_stations_and_times(csv_df, month_year):
    csv_df = clean_data(csv_df)
    peak_hours = csv_df.groupby(csv_df['Hora_Retiro'].dt.hour).size()
    peak_hours.plot(kind='bar', title='Horario más Saturado ' + month_year)
    plt.xlabel('Hora del Retiro')
    plt.ylabel('Número de viajes')
    plt.savefig(month_year + '_traffic_at_the_most_congested_stations_and_times.png')
    plt.show()


if __name__ == '__main__':
    # Read data
    november_df = pd.read_csv('datos_abiertos_2023_diciembre.csv')
    december_df = pd.read_csv('datosabiertos_2023_noviembre.csv')

    #
    # The following lines are commented because I thought about analyzing the data
    # from the months together, but in point 4 it says: "Compare the results you found
    # between the tables of the two months you downloaded."
    #

    # # Concatenate the dataframes
    # dataframes = [november_df, december_df]
    # combined_df = pd.concat(dataframes)
    #
    # # Clean data
    # combined_df['Ciclo_Estacion_Retiro'] = combined_df['Ciclo_Estacion_Retiro'].apply(lambda x: x.split('-')[0])
    # combined_df['Ciclo_EstacionArribo'] = combined_df['Ciclo_EstacionArribo'].apply(lambda x: x.split('-')[0])
    #
    # # Convert date and time columns to datetime type
    # combined_df['Fecha_Retiro'] = pd.to_datetime(combined_df['Fecha_Retiro'], format='%d/%m/%Y')
    # combined_df['Hora_Retiro'] = pd.to_datetime(combined_df['Hora_Retiro'], format='%H:%M:%S')
    # combined_df['Fecha Arribo'] = pd.to_datetime(combined_df['Fecha Arribo'], format='%d/%m/%Y')
    # combined_df['Hora_Arribo'] = pd.to_datetime(combined_df['Hora_Arribo'], format='%H:%M:%S')

    # 1. Most saturated stations
    # Most congested arrival stations.
    most_congested_arrival_stations(december_df, "December_2023")
    most_congested_arrival_stations(november_df, "November_2023")

    # Most congested withdrawal stations
    most_congested_withdrawal_stations(december_df, "December_2023")
    most_congested_withdrawal_stations(november_df, "November_2023")

    # 2. Most frequented routes
    most_frequented_routes(december_df, "December_2023")
    most_frequented_routes(november_df, "November_2023")

    # 3. Traffic at the most congested stations and times.
    # Traffic at the most used stations.
    traffic_at_the_most_used_stations(december_df, "December_2023")
    traffic_at_the_most_used_stations(november_df, "November_2023")

    # Traffic at the most congested stations and times.
    traffic_at_the_most_congested_stations_and_times(december_df, "December_2023")
    traffic_at_the_most_congested_stations_and_times(november_df, "November_2023")

    # Analyze the most used station per month
    more_used_stations(december_df, "December_2023")
    more_used_stations(november_df, "November_2023")

    # Bike wear per year
    bike_wear_per_year(december_df, "December_2023")
    bike_wear_per_year(november_df, "November_2023")

    # explore_relationships_between_gender_and_age_of_users
    explore_relationships_between_gender_and_age_of_users(december_df, "December_2023")
    explore_relationships_between_gender_and_age_of_users(november_df, "November_2023")




