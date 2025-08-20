CREATE MIGRATION m1rs3ylfpjv6evjnlz7srxezbp5emdpg6kujnveyil6l7nh7o4zzsq
    ONTO initial
{
  CREATE SCALAR TYPE default::GenderEnum EXTENDING enum<male, female>;
  CREATE SCALAR TYPE default::GenreEnum EXTENDING enum<SF, Romantic, Action, Comedy, Horror, Adventure>;
  CREATE FUTURE simple_scoping;
  CREATE ABSTRACT TYPE default::BaseModel {
      CREATE REQUIRED PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
      };
  };
  CREATE TYPE default::Movie EXTENDING default::BaseModel {
      CREATE REQUIRED PROPERTY cast: std::json;
      CREATE REQUIRED PROPERTY genre: default::GenreEnum;
      CREATE REQUIRED PROPERTY playtime: std::int16;
      CREATE REQUIRED PROPERTY plot: std::str;
      CREATE REQUIRED PROPERTY title: std::str {
          CREATE CONSTRAINT std::max_len_value(255);
      };
  };
  CREATE TYPE default::User EXTENDING default::BaseModel {
      CREATE REQUIRED PROPERTY age: std::int16;
      CREATE REQUIRED PROPERTY gender: default::GenderEnum;
      CREATE REQUIRED PROPERTY hashed_password: std::str;
      CREATE OPTIONAL PROPERTY last_login: std::datetime;
      CREATE REQUIRED PROPERTY username: std::str {
          CREATE CONSTRAINT std::exclusive;
          CREATE CONSTRAINT std::max_len_value(50);
      };
  };
};
