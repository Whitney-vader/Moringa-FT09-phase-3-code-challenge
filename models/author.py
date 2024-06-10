from database.connection import get_db_connection


class Author:
    all = {}

    def __init__(self, id, name):
        self._id = id
        self._name = name

    def __repr__(self):
        return f'<Author {self.id} {self.name}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed after initializing")
        else:
            if isinstance(new_name, str):
                if len(new_name) > 0:
                    self._name = new_name

    def save(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            INSERT INTO authors (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        conn.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name):
        author = cls(None, name)
        author.save()
        return author

    def get_author_id(self):
        return self.id

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT ar.*
            FROM articles ar
            INNER JOIN authors a ON ar.author = a.id
            WHERE a.id =?
        """
        CURSOR.execute(sql, (self.id,))
        article_data = CURSOR.fetchall()
        articles = []
        for row in article_data:
            articles.append(Article(*row))
        return articles

    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT DISTINCT m.*
            FROM magazines m
            INNER JOIN articles ar ON ar.magazine = m.id
            INNER JOIN authors a ON ar.author = a.id
            WHERE a.id =?
        """
        CURSOR.execute(sql, (self.id,))
        magazine_data = CURSOR.fetchall()
        magazines = []
        for row in magazine_data:
            magazines.append(Magazine(*row))
        return magazines

    def update(self):
        conn = get_db_connection()
        sql = """
            UPDATE authors
            SET name =?
            WHERE id =?
        """
        cur = conn.cursor()
        cur.execute(sql, (self.name, self.id))
        conn.commit()

    def delete(self):
        conn = get_db_connection()
        sql = """
            DELETE FROM authors
            WHERE id =?
        """
        cur = conn.cursor()
        cur.execute(sql, (self.id,))
        conn.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def find_by_id(cls, author_id):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM authors
            WHERE id =?
        """
        CURSOR.execute(sql, (author_id,))
        author_data = CURSOR.fetchone()
        if author_data:
            return cls(*author_data)
        else:
            return None