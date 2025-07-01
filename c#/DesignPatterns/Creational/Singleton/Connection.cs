namespace Singleton
{
    //Ensure a class has only one instance and provide a global point of access to it.
    class Connection
    {
        private static Connection _instance;
        // Lock synchronization object
        private static object syncLock = new object();
        // Constructor (protected)
        public static int index { get; private set; }
        protected Connection()
        {
            index += 1;
        }
        public static Connection GetConnection()
        {
            // Support multithreaded applications through
            // 'Double checked locking' pattern which (once
            // the instance exists) avoids locking each
            // time the method is invoked

            if (_instance == null)
            {
                lock (syncLock)
                {
                    if (_instance == null)
                    {
                        _instance = new Connection();
                    }
                }
            }
            return _instance;
        }
    }
}
