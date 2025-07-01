using System;
using System.Collections.Generic;
using System.Text;

namespace Factory.Method
{
    public abstract class Table
    {
        public abstract void Legs();
        public abstract void Look();
    }
    public class ModernTable : Table
    {
        public override void Legs()
        {
        }
        public override void Look()
        {
        }
    }
    public class ClassicTable : Table
    {
        public override void Legs()
        {
        }
        public override void Look()
        {
        }
    }
}
