import psycopg

conn = psycopg.connect(dbname='repro', autocommit=True)
conn.execute('DROP TABLE IF EXISTS items')
conn.execute('CREATE TABLE items (id bigserial, description text)')

description = 'test' * 100

cur = conn.cursor()
with cur.copy('COPY items (description) FROM STDIN WITH (FORMAT BINARY)') as copy:
    copy.set_types(['text'])

    for i in range(1000000):
        # show progress
        if i % 10000 == 0:
            print('.', end='', flush=True)

        copy.write_row([description])

print()
