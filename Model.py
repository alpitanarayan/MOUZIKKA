import cx_Oracle
class Model:
    def __init__(self):
        self.song_dict = {}
        self.db_status=True
        self.conn=None
        self.cur=None

        try:
            self.conn = cx_Oracle.connect("c##mouzikka/music@127.0.0.1/orcl")
            self.cur = self.conn.cursor()
            print("Connected to DB successfully")
            self.cur.execute("select * from c##mouzikka.myfavourites")
            tables_names = self.cur.fetchall()
            for table_name in tables_names:
                print(table_name)

        except cx_Oracle.DatabaseError as e:
            self.db_status = False
            print("Database Error:", e)

    # def create_table_if_not_exists(self):
    #     # Create Table 'myfavourites' if it doesn't exist
    #     create_table_query = '''
    #         CREATE TABLE myfavourites (
    #             song_id NUMBER,
    #             song_name VARCHAR2(100),
    #             song_path VARCHAR2(100)
    #         )
    #     '''
    #     try:
    #         self.cur.execute(create_table_query)
    #         self.conn.commit()  # Remember to commit the changes
    #         print("Table 'myfavourites' created successfully or already exists.")
    #     except cx_Oracle.DatabaseError as e:
    #         print("Table creation error:", e)


    def get_db_status(self):
        return self.db_status
    def close_db_conn(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()
        print("Disconnected with the DB")

    def add_song(self,song_name,song_path):
        self.song_dict[song_name] = song_path

    def get_song_path(self,song_name):
        return self.song_dict[song_name]

    def remove_song(self,song_name):
        self.song_dict.pop(song_name)


    def search_song_in_favourites(self,song_name):
        self.cur.execute("Select song_name from myfavourites where song_name=:1",(song_name,))
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        return True;

    def add_song_in_favourites(self,song_name,song_path):
        is_song_present = self.search_song_in_favourites(song_name)    #may return True or False ---> if it return false then--->
        if is_song_present:                                            #if also become false then we search foe max_song
            return "Song already present in favourites"
        self.cur.execute("Select max(song_id) from myfavourites")
        result = self.cur.fetchone()
        last_song_id = result[0]
        next_song_id = 1
        if last_song_id is not None:
            next_song_id = last_song_id + 1
        self.cur.execute("insert into myfavourites values(:1,:2,:3)",(next_song_id,song_name,song_path))
        self.conn.commit()
        # record added
        return "song added to favorites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myfavourites")
        songs_present = False
        # x = len(self.song_dict)   ---->This x used for 2nd method
        # for self.x in cur:                                         #x contain tuple
        for song_name,song_path in self.cur:
            self.song_dict[song_name] = song_path
            songs_present = True

        #check weather the song is added in favourites
        #method 1:(best)

        if songs_present:
            return "List populated with favourites"
        else:
            return "No songs present in favourites"



        # check weather the song is added in favourites
        # method 1:

        # y = len(self.song_dict)
        # if x!=y:
        #     return "List populated with favourites"
        # else:
        #     return "No songs present in favourites"



    def remove_song_from_favourite(self, song_name):
        self.cur.execute("delete from myfavourites where song_name=:1",(song_name,))

        if self.cur.rowcount == 0:                #this song is not part of favourite
            return "song not present in your favourites"
        self.song_dict.pop(song_name)
        #commit the data to delete the data -->
        self.conn.commit()
        return "song deleted from your favourites "

    def get_song_count(self):
        return len(self.song_dict)




















