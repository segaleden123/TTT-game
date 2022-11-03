class ZooKeeperREST_TestCase(unittest.TestCase):
    
    BASE_URI = 'http://localhost:9998'

    def setUp(self):
        self.zk = ZooKeeper(self.BASE_URI)

    def tearDown(self):
        try:
            self.zk.delete('/test')
        except ZooKeeper.NotFound:
            pass

    def test_get_root_node(self):
        assert self.zk.get('/') is not None

    def test_get_node_not_found(self):
        self.assertRaises(ZooKeeper.NotFound, \
            self.zk.get, '/dummy-node')

    def test_exists_node(self):
        assert self.zk.exists('/zookeeper') is True

    def test_get_children(self):
        assert any([child['path'] == '/zookeeper/quota' \
            for child in self.zk.get_children('/zookeeper')])
            
    def test_create_znode(self):
        try:
            self.zk.create('/test')
        except ZooKeeper.ZNodeExists:
            pass # it's ok if already exists
        assert self.zk.exists('/test') is True

   
    def test_set_with_older_version(self):
        if not self.zk.exists('/test'):
            self.zk.create('/test', 'random-data')

        zn = self.zk.get('/test')
        self.zk.set('/test', 'new-data')
        self.assertRaises(ZooKeeper.WrongVersion, self.zk.set, \
            '/test', 'older-version', version=zn['version'])

    def test_set_null(self):
        if not self.zk.exists('/test'):
            self.zk.create('/test', 'random-data')
        self.zk.set('/test', 'data')
        assert 'data64' in self.zk.get('/test')

        self.zk.set('/test', null=True)
        assert 'data64' not in self.zk.get('/test')
        
    def test_presence_signaling(self):
        with self.zk.session(expire=1):
            self.zk.create('/i-am-online', ephemeral=True)
            assert self.zk.exists('/i-am-online')
        assert not self.zk.exists('/i-am-online')
