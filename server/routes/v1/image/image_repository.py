from sqlalchemy.ext.asyncio import AsyncSession

from routes.v1.image.dto.scan_request import ScanRequest
from schemas.scan import Scan



class ImageRepository:

    async def create(
        self,
        user_id: int,
        data: ScanRequest,
        db : AsyncSession
    ) -> Scan:

        scan = Scan(
            user_id=user_id,
            image_url=data.image_url,
            predicted_class=data.predicted_class,
            cause=data.cause,
            prescriptions=data.prescriptions
        )

        db.add(scan)
        
        await db.commit()

        await db.refresh(scan)
        print(scan)

        return scan
