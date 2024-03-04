require "pg"

conn = PG.connect(dbname: "repro")
conn.exec("DROP TABLE IF EXISTS items")
conn.exec("CREATE TABLE items (id bigserial, description text)")

description = "test" * 100

coder = PG::BinaryEncoder::CopyRow.new
conn.copy_data("COPY items (description) FROM STDIN WITH (FORMAT BINARY)", coder) do
  1000000.times do |i|
    # show progress
    putc "." if i % 10000 == 0

    conn.put_copy_data([description])
  end
end

puts
