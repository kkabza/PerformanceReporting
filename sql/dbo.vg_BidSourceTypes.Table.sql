USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_BidSourceTypes]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_BidSourceTypes](
	[BidSourceID] [int] IDENTITY(1,1) NOT NULL,
	[BidSourceName] [varchar](50) NOT NULL
) ON [PRIMARY]
GO
