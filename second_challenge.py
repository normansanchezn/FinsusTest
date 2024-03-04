if __name__ == '__main__':
    # Demographic data for each AGEB
    poblacion_ageb = {
        'AGEB1': 1000,
        'AGEB2': 1500,
        # Add more population data for each AGEB
    }

    # Birth rate for the region
    birth_rate_region = 0.025  # Example: 2.5% birth rate

    # Population distribution within the 0-6 months age range
    # Let's assume 10% of the total population is within this age range
    proportion_0_6_months = 0.1

    # Calculate the estimation of infants aged 0-6 months for each AGEB
    infant_estimation_ageb = {}
    for ageb, population in poblacion_ageb.items():
        infant_estimation_ageb[ageb] = population * birth_rate_region * proportion_0_6_months

    # Display results
    print("Estimation of infants aged 0-6 months in each Basic Geostatistical Area (AGEB):")
    for ageb, estimation in infant_estimation_ageb.items():
        print(f"AGEB {ageb}: {estimation} infants")