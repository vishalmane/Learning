using System;

namespace Adapter
{
    class PlayStationController : PSController
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
    class PlayStation : Console
    {
        public PlayStation()
        {
            // Associate new PlayStationController as default.
            Controller = new PlayStationController();
        }      

        public override void Play()
        {
        }
    }

}
