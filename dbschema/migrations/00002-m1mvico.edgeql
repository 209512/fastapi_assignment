CREATE MIGRATION m1mvico3arlndkoipcvjbscphzkgkz7fgljudml5gdwhfxvnzy232a
    ONTO m1rs3ylfpjv6evjnlz7srxezbp5emdpg6kujnveyil6l7nh7o4zzsq
{
  CREATE TYPE default::Review {
      CREATE REQUIRED LINK movie: default::Movie;
      CREATE REQUIRED LINK user: default::User;
      CREATE REQUIRED PROPERTY content: std::str {
          CREATE CONSTRAINT std::max_len_value(255);
      };
      CREATE REQUIRED PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE PROPERTY review_image_url: std::str;
      CREATE REQUIRED PROPERTY title: std::str {
          CREATE CONSTRAINT std::max_len_value(50);
      };
  };
  CREATE TYPE default::ReviewLike {
      CREATE REQUIRED LINK review: default::Review;
      CREATE REQUIRED LINK user: default::User;
      CREATE REQUIRED PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY is_liked: std::bool {
          SET default := true;
      };
  };
};
