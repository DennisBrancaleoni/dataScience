import pandas as pd

results      = pd.read_csv('data/results.csv',              na_values='\\N')
races        = pd.read_csv('data/races.csv',                na_values='\\N')
drivers      = pd.read_csv('data/drivers.csv',              na_values='\\N')
constructors = pd.read_csv('data/constructors.csv',         na_values='\\N')
circuits     = pd.read_csv('data/circuits.csv',             na_values='\\N')
qualifying   = pd.read_csv('data/qualifying.csv',           na_values='\\N')
pit_stops    = pd.read_csv('data/pit_stops.csv',            na_values='\\N')
status       = pd.read_csv('data/status.csv',               na_values='\\N')
driver_std   = pd.read_csv('data/driver_standings.csv',     na_values='\\N')
constr_std   = pd.read_csv('data/constructor_standings.csv',na_values='\\N')

# --- 2. Aggregazione pit stop (per pilota per gara) ---
pit_agg = pit_stops.groupby(['raceId', 'driverId']).agg(
    pit_stop_count   = ('stop',         'max'),
    total_pit_time_ms= ('milliseconds', 'sum')
).reset_index()

# --- 3. Qualifying: rinomina colonne per chiarezza ---
quali_clean = qualifying[['raceId', 'driverId', 'position', 'q1', 'q2', 'q3']].copy()
quali_clean.columns = ['raceId', 'driverId', 'quali_position', 'quali_q1', 'quali_q2', 'quali_q3']

# --- 4. Classifica piloti a fine gara ---
ds = driver_std[['raceId', 'driverId', 'points', 'position', 'wins']].copy()
ds.columns = ['raceId', 'driverId', 'driver_champ_points', 'driver_champ_position', 'driver_champ_wins']

# --- 5. Classifica costruttori a fine gara ---
cs = constr_std[['raceId', 'constructorId', 'points', 'position', 'wins']].copy()
cs.columns = ['raceId', 'constructorId', 'constr_champ_points', 'constr_champ_position', 'constr_champ_wins']

# --- 6. JOIN principale ---
df = results.merge(
    races[['raceId', 'year', 'round', 'circuitId', 'name', 'date']],
    on='raceId', how='left')

df = df.merge(
    circuits[['circuitId', 'name', 'location', 'country', 'lat', 'lng', 'alt']],
    on='circuitId', how='left', suffixes=('_race', '_circuit'))

df = df.merge(
    drivers[['driverId', 'driverRef', 'code', 'forename', 'surname', 'dob', 'nationality']],
    on='driverId', how='left')

df = df.merge(
    constructors[['constructorId', 'name', 'nationality']],
    on='constructorId', how='left', suffixes=('', '_constructor'))

df = df.merge(status[['statusId', 'status']], on='statusId', how='left')
df = df.merge(quali_clean,  on=['raceId', 'driverId'],      how='left')
df = df.merge(pit_agg,      on=['raceId', 'driverId'],      how='left')
df = df.merge(ds,           on=['raceId', 'driverId'],      how='left')
df = df.merge(cs,           on=['raceId', 'constructorId'], how='left')

# --- 7. Rinomina colonne ---
df = df.rename(columns={
    'name_race':              'race_name',
    'name_circuit':           'circuit_name',
    'name':                   'constructor_name',
    'nationality':            'driver_nationality',
    'nationality_constructor':'constructor_nationality',
    'time':                   'race_finish_time',
    'milliseconds':           'race_time_ms',
    'laps':                   'laps_completed',
    'grid':                   'start_position',
    'position':               'finish_position',
    'positionOrder':          'finish_order',
    'positionText':           'finish_position_text',
    'rank':                   'fastest_lap_rank',
    'fastestLap':             'fastest_lap_number',
    'fastestLapTime':         'fastest_lap_time',
    'fastestLapSpeed':        'fastest_lap_speed_kmh',
    'points':                 'points_scored',
    'date':                   'race_date',
    'lat':                    'circuit_lat',
    'lng':                    'circuit_lng',
    'alt':                    'circuit_alt_m',
    'dob':                    'driver_dob',
    'code':                   'driver_code',
    'forename':               'driver_forename',
    'surname':                'driver_surname',
    'driverRef':              'driver_ref',
    'number':                 'car_number',
})

# --- 8. Rimozione colonne ID ridondanti dopo il join ---
df = df.drop(columns=['resultId', 'statusId', 'circuitId'])

# --- 9. Ordinamento cronologico ---
df = df.sort_values(['year', 'round', 'finish_order']).reset_index(drop=True)

# --- 10. Salvataggio ---
output_path = 'mainDataset.csv'
df.to_csv(output_path, index=False)

print(f"Dataset salvato: {output_path}")
print(f"   Righe:   {len(df):,}")
print(f"   Colonne: {len(df.columns)}")