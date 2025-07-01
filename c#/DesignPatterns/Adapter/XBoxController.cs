using System;

namespace Adapter
{

    class XBoxController : XController
    {
        public override void DownBtnClick()
        {
            throw new NotImplementedException();
        }

        public override void LetfBtnClick()
        {
            throw new NotImplementedException();
        }

        public override void RightBtnClick()
        {
            throw new NotImplementedException();
        }

        public override void UpBtnClick()
        {
            throw new NotImplementedException();
        }
    }

    class XBox : Console
    {
        public XBox()
        {
            // Associate new XBoxController as default.
            Controller = new XBoxController();
        }       
        public override void Play()
        {
          
        }
    }

}
